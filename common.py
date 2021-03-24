from string import Template
import json

from db import DB


def get_livre():
    with open('livre.json', 'r') as f:
        livre = json.load(f)
        return livre


def get_cautions():
    with open('cautions.json', 'r') as f:
        livre = json.load(f)
        return livre


def get_signature(officer):
    character = DB().get_character(name=officer)
    if character.get('signature') is None:
        del character['signature']
    return character.get('signature', officer)


def get_grade(officer):
    character = DB().get_character(name=officer)
    if character.get('grade') is None:
        del character['grade']
    return character.get('grade', 'Aucun')


def get_assignation(officer):
    character = DB().get_character(name=officer)
    if character.get('assignation') is None:
        del character['assignation']
    return character.get('assignation', 'Aucun')


def get_matricule(officer):
    character = DB().get_character(name=officer)
    if character.get('matricule') is None:
        del character['matricule']
    return character.get('matricule', '#')


def find_occurences(lines, query, by_number=False):
    query = query.strip()
    occurences = []
    mini_queries = query.split(' ')
    if by_number:
        for line in lines:
            try:
                if line.split('.')[0] == query.strip():
                    occurences.append(line)
            except IndexError:
                pass
    else:
        for line in lines:
            correspond = True
            for mini_query in mini_queries:
                if line.lower().find(mini_query.lower()) == -1:
                    correspond = False
            if correspond:
                occurences.append(line)
    return occurences


def find_charge(query):
    with open('livre', 'r') as f:
        lines = f.readlines()
        charges = find_occurences(lines, query)
        return charges


def find_article(query):
    with open('code_route', 'r') as f:
        lines = f.readlines()
        articles = find_occurences(lines, query, by_number=True)
    with open('code_penal', 'r') as f:
        lines = f.readlines()
        articles.extend(find_occurences(lines, query, by_number=True))
    return articles


def find_caution(query):
    with open('cautions', 'r') as f:
        lines = f.readlines()
        cautions = find_occurences(lines, query)
        return cautions


def instantiate_template(template, args):
    with open(template) as template_file:
        src = Template(template_file.read())
        result = src.substitute(args)
        return result


def saisie_to_str(saisie):
    return ' {} '.format(saisie) if saisie != 0 else '  '
