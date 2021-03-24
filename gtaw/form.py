import shlex
import discord

from config import Config
from db import DB
from seal import Seal
from string import Template
from datetime import datetime


class Form:

    def __init__(self, command, message, seal=Seal.LSPD, officer=None):
        self.command = command
        self.command_example = Config.forms[command]["command_example"]

        self.template_filepath = Config.forms[command]["template_filepath"]
        self.template_args = Config.forms[command].get("template_args", [])
        self.template_optional_args = Config.forms[command].get("template_optional_args", [])
        self.template_link = Config.forms[command].get("template_link", "*Lien à venir*")

        self.seal = seal

        self.parameters = {}

        self.date = datetime.today().strftime("%d/%b/%Y à %H:%M").upper()

        self.officer = officer
        self.static_parameters = {"officer": self.officer}
        if self.officer is not None:
            character = DB().get_character(name=self.officer)
            self.grade = character.get('grade')
            if character.get('signature') is None:
                self.signature = self.officer
            else:
                self.signature = character.get('signature')
            if character.get('matricule') is None:
                self.matricule = "#Aucun"
            else:
                self.matricule = "#{}".format(character.get('matricule'))
            self.static_parameters.update({
                "grade": self.grade,
                "signature": self.signature,
                "matricule": self.matricule
            })

        self.args = self._get_args(message)

    def _get_args(self, message):
        args = shlex.split(message)
        template_values = args[1:len(self.template_args) + 1]
        template_optional_values = args[len(self.template_args) + 1:]

        self.parameters.update(dict(zip(self.template_args, template_values)))
        # fill optional parameters with default
        for template_optional_arg in self.template_optional_args:
            self.parameters.update(template_optional_arg)
        # fill optional parameters with provided args
        for template_optional_value in template_optional_values:
            if template_optional_value.find('=') != -1:
                optional_arg = template_optional_value.split("=")
                self.parameters.update({optional_arg[0]: optional_arg[1]})

        return self.parameters

    def generate(self):
        messages = []
        if len(self.parameters) < len(self.template_args):
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(210, 190, 100),
                title=":information_source: Syntaxe",
                description="La commande doit respecter le format ci-dessous.\n"
                            "**Les paramètres comprenant un ou plusieurs espace(s) "
                            "doivent être entourés de guillemets.**"
            )
            embed.set_thumbnail(url=str(self.seal))
            embed.add_field(name="Paramètres", value="{}".format(self._get_syntax()),
                            inline=False)
            embed.add_field(name="Exemple", value="```#{} {}```".format(self.command, self.command_example),
                            inline=False)
            if self.command == "arrestation":
                embed.add_field(name="Plaidoiries possibles",
                                value="`Coupable sans commis d'office`\u200b\n"
                                      "`Coupable avec commis d'office`\u200b\n"
                                      "`Non-Coupable sans commis d'office`\u200b\n"
                                      "`Non-Coupable avec commis d'office`",
                                inline=False)
            embed = self._feedback_parameters(embed)
            return messages, embed

        with open(self.template_filepath, 'r') as template_file:
            src = Template(template_file.read())
            self.parameters.update(self.static_parameters)
            self.parameters.update({"date": self.date})
            result = src.substitute(self.parameters)
            lines = [line + "\n" for line in result.split('\n')]
            max_char = 1000
            for line in lines:
                if len(messages) <= 0:
                    messages.append(line)
                    continue

                last_line = len(messages) - 1
                if len(messages[last_line]) < max_char:
                    messages[last_line] = messages[last_line] + line
                else:
                    messages.append(line)

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(210, 190, 100),
            title=":printer: Impression d'un formulaire ({})".format(self.command),
            description="Fait par {} {} le {}".format(
                self.grade, self.officer, self.date)
        )
        embed.set_thumbnail(url=str(Seal.LSPD))
        embed = self._feedback_parameters(embed)
        if self.command == "arrestation":
            suspect_name = self.parameters.get("suspect")
            suspect_name_url = suspect_name.replace(' ', '_')
            embed.add_field(name="A mettre dans le MDC ici (Actions > Créer un casier > Type = Rapport d'arrestation)",
                            value="https://mdc-fr.gta.world/record/{}".format(suspect_name_url),
                            inline=False)
            embed.add_field(name="MEA **Copiez le texte que vous avez collé dans le MDC, ici**",
                            value="https://forum-fr.gta.world/index.php?/forum/201-demandes-de-mise-en-accusation/&do=add",
                            inline=False)
            embed.add_field(name="Titre",
                            value="```Demande de mise en accusation - {}```".format(suspect_name.upper()), inline=False)
            embed.set_footer(text="Suivez les étapes ci-dessus et voilà !")
        else:
            embed.add_field(name="A soumettre ici",
                            value="{}".format(self.template_link), inline=False)
            embed.set_footer(text="Copiez, cliquez sur le lien, collez et soumettez, voilà !")

        return messages, embed

    def _get_syntax(self):
        args = ['<{}>'.format(template_arg) for template_arg in self.template_args]
        optional_args = ['<{} ({} par défaut)>'.format(
            list(template_optional_arg.keys())[0], list(template_optional_arg.values())[0])
                         for template_optional_arg in self.template_optional_args]
        args_str = ' '.join(args + optional_args)
        return "```#{} {}```".format(self.command, args_str)

    def _get_parameters(self):
        parameters_str = ""
        for key, value in self.parameters.items():
            parameters_str = parameters_str + "`{}` = `{}`\n".format(key, value)
        return parameters_str

    def _feedback_parameters(self, embed):
        if len(self.parameters) > 0:
            embed.add_field(name="Valeur des paramètres",
                            value="{}".format(self._get_parameters()),
                            inline=False)
        missing_args = ['`{}`'.format(template_arg if template_arg != "" else " ")
                        for template_arg in self.template_args if template_arg not in self.parameters.keys()]
        if len(missing_args) > 0:
            embed.add_field(name="Paramètres manquants",
                            value="{}".format(' '.join(missing_args)),
                            inline=False)
        return embed
