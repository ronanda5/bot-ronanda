import json
import os
import time

import requests
from bs4 import BeautifulSoup
import re


class Law:
    LAW_CONTENT_FILE = "law"
    LAW_DICT_FILE = "law.json"

    def __init__(self, force=False):
        if not os.path.exists(self.LAW_DICT_FILE) or force:
            # retrieve laws from internet
            links = [
                # PENAL
                "https://forum-fr.gta.world/index.php?/topic/344-titre-01-dispositions-g%C3%A9n%C3%A9rales-de-proc%C3%A9dure-p%C3%A9nale/",
                "https://forum-fr.gta.world/index.php?/topic/346-titre-02-enqu%C3%AAte-criminelle/",
                "https://forum-fr.gta.world/index.php?/topic/347-titre-03-poursuite-des-infractions-p%C3%A9nales/",
                "https://forum-fr.gta.world/index.php?/topic/374-titre-04-appel-certiorari/",
                "https://forum-fr.gta.world/index.php?/topic/348-titre-05-proc%C3%A9dures-sp%C3%A9cifiques/",
                "https://forum-fr.gta.world/index.php?/topic/349-titre-06-ex%C3%A9cution-des-d%C3%A9cisions-de-justice/",
                "https://forum-fr.gta.world/index.php?/topic/350-titre-07-fichiers-criminels/",
                "https://forum-fr.gta.world/index.php?/topic/351-titre-08-peine-de-mort/",
                "https://forum-fr.gta.world/index.php?/topic/353-titre-09-polices-institu%C3%A9es/",
                "https://forum-fr.gta.world/index.php?/topic/360-titre-10-droit-p%C3%A9nal-g%C3%A9n%C3%A9ral/",
                "https://forum-fr.gta.world/index.php?/topic/384-titre-11-principales-infractions-p%C3%A9nales/",
                "https://forum-fr.gta.world/index.php?/topic/421-titre-12-circulation-routi%C3%A8re-a%C3%A9rienne-fluviale-et-maritime/",
                "https://forum-fr.gta.world/index.php?/topic/422-titre-13-r%C3%A9pression-des-conspirations-criminelles/",
                # CIVIL
                "https://forum-fr.gta.world/index.php?/topic/469-titre-01-dispositions-g%C3%A9n%C3%A9rales/",
                "https://forum-fr.gta.world/index.php?/topic/472-titre-02-proc%C3%A9dure-civile/",
                "https://forum-fr.gta.world/index.php?/topic/357-titre-03-ordre-des-avocats/",
                "https://forum-fr.gta.world/index.php?/topic/534-titre-04-responsablit%C3%A9-civile/",
                "https://forum-fr.gta.world/index.php?/topic/535-titre-05-droit-du-travail/",
                "https://forum-fr.gta.world/index.php?/topic/536-titre-06-droit-des-personnes/",
                "https://forum-fr.gta.world/index.php?/topic/543-titre-07-transparence-de-la-vie-publique/",
                # ORDRES
                "https://forum-fr.gta.world/index.php?/topic/598-cash-loi-relative-au-commerce-%C3%A0-lactivit%C3%A9-des-soci%C3%A9t%C3%A9s-et-aux-holdings/",
                "https://forum-fr.gta.world/index.php?/topic/419-landa-loi-relative-aux-armes-%C3%A0-leur-num%C3%A9rotation-%C3%A0-leur-distribution-et-%C3%A0-leur-acquisition/",
                "https://forum-fr.gta.world/index.php?/topic/544-l%C5%93-loi-relative-%C3%A0-lordre-de-l%C3%A9quit%C3%A9/",
                "https://forum-fr.gta.world/index.php?/topic/602-pipe-loi-relative-%C3%A0-la-prostitution-et-aux-imp%C3%A9ratifs-des-prox%C3%A9n%C3%A8tes-employeurs/",
                "https://forum-fr.gta.world/index.php?/topic/417-pls-loi-relative-%C3%A0-la-prescription-l%C3%A9gale-de-stup%C3%A9fiants/",
            ]
            content = ""
            for link in links:
                source = requests.get(link)
                self.soup = BeautifulSoup(source.text, "lxml")
                print("{} {}".format(self.soup.title.text, "(loaded)"))
                posts = self.soup.find_all("div", class_="cPost_contentWrap")
                for post in posts:
                    content = content + post.get_text().replace(" v. ", " v ")
                content = content + "\n"
                time.sleep(2)

            # write all law in file
            with open(self.LAW_CONTENT_FILE, 'w') as law_file:
                law_file.write(content)

            with open(self.LAW_CONTENT_FILE, 'r') as law_file:
                self.laws = law_file.readlines()

            articles = {}
            article = None
            for line in self.laws:

                find_article = re.match("(^[0-9]+(-[0-9]+)?\. [^.]+\.)(.*)", line)
                if find_article:
                    if article is not None:
                        articles[article] = articles[article].strip()\
                            .replace("              ", "\n")\
                            .replace(":                 ", "\n")\
                            .replace(r'\n+', '\n')
                    # article_full = find_article.group(0)
                    article_title = find_article.group(1).strip()
                    # article_subnumber = find_article.group(2).strip()
                    article_content = find_article.group(3).strip()
                    article = article_title
                    print("{} {}".format(article, "(saved)"))
                    articles[article] = article_content.strip()
                elif article is not None:
                    if line == " \n":
                        article = None
                        continue
                    if line.startswith("Modifié") \
                            or line.startswith("Hon.") \
                            or line.startswith("Juge en chef") \
                            or line.startswith("Chapitre"):
                        continue
                    articles[article] = articles[article] + line

            with open(self.LAW_DICT_FILE, 'w') as outfile:
                json.dump(articles, outfile, indent=4)

            os.remove(self.LAW_CONTENT_FILE)

    @staticmethod
    def find(query):

        with open(Law.LAW_DICT_FILE, 'r') as outfile:
            articles = json.load(outfile)

        occurrences = {}
        for title, content in articles.items():
            if query.lower() not in title.lower() and query.lower() not in content.lower():
                continue
            occurrences[title] = content
        return occurrences
