import shlex
import discord

from commands.command import EnumCommand
from config import Config
from seal import Seal
from string import Template
from datetime import datetime


class Form:

    def __init__(self, command: EnumCommand, message, seal=Seal.LSPD, character=None):
        self.command = command
        self.command_example = Config.forms[command]["command_example"]

        self.template_filepath = Config.forms[command]["template_filepath"]
        self.template_args = Config.forms[command].get("template_args", [])
        self.template_link = Config.forms[command].get("template_link", "*Lien à venir*")
        self.instructions = Config.forms[command].get("instructions", [])

        self.seal = seal

        self.parameters = {}

        self.date = datetime.today().strftime("%d/%b/%Y à %H:%M").upper()

        self.officer = character.get('name')
        self.static_parameters = {"officer": self.officer}
        if self.officer is not None:
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

        self.parameters.update(dict(zip(self.template_args, template_values)))

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
            embed.add_field(name="Exemple", value="```#{} {}```".format(self.command.value, self.command_example),
                            inline=False)
            if self.command == EnumCommand.ARREST:
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
            title=":printer: Impression d'un formulaire ({})".format(self.command.value),
            description="Fait par {} {} le {}".format(
                self.grade, self.officer, self.date)
        )
        embed.set_thumbnail(url=str(Seal.LSPD))

        embed = self._feedback_parameters(embed)

        suspect_name = self.parameters.get("suspect")
        for instruction in self.instructions:
            instruction_name = instruction["name"]
            instruction_value = instruction["value"]
            if suspect_name is not None:
                instruction_value = instruction_value.format(suspect_name_url=suspect_name.replace(' ', '_'),
                                                             suspect_name=suspect_name.upper())
            embed.add_field(name=instruction_name,
                            value=instruction_value,
                            inline=False)
        embed.set_footer(text="Suivez les instructions ci-dessus et voilà !")

        return messages, embed

    def _get_syntax(self):
        args = ['<{}>'.format(template_arg) for template_arg in self.template_args]
        args_str = ' '.join(args)
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
