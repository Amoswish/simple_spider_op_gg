import re
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from simpleSpider_op_gg.items import SimplespiderOpGgItem
import json
import os
class Myspider(scrapy.Spider):
    name = 'simpleSpider_op_gg'
    # https: // pubg.op.gg / leaderboard /?platform = steam & mode = fpp & queue_size = 1
    allowed_domains = ['pubg.op.gg']
    bash_url = 'https://pubg.op.gg/leaderboard/?platform=steam&'
    play_mode = ['tpp','fpp']
    play_teamsize = ['1','2','4']
    # play_mode = ['tpp']
    # play_teamsize = ['1']
    bashurl = '.html'
    def start_requests(self):
        for item_mode in self.play_mode :
            for item_teamsize in self.play_teamsize:
                url = self.bash_url + 'mode=' + item_mode + '&queue_size=' + item_teamsize
                yield Request(url,self.parse,meta={'mode':item_mode,'teamsize':item_teamsize})
                print(item_mode+item_teamsize)

    def parse(self, response):
        page = BeautifulSoup(response.text)
        # item = SimplespiderOpGgItem()
        leaderboard = []
        leaderboard_top_3 = page.find_all('li',attrs={'class':'leader-board-top3__item '})
        for i,item_top3 in enumerate(leaderboard_top_3):
            templeaderboardrow = []
            # 用户排名
            playerrank = item_top3.find('span',attrs={'class':'leader-board-top3__rank'}).get_text()
            templeaderboardrow.append(playerrank)
            # 用户id

            playerid = item_top3.find('span',attrs={'class':'leader-board-top3__nickname'}).find('a').get_text()
            templeaderboardrow.append(playerid)
            # sp
            plyaersp = item_top3.find('span',attrs={'class':'leader-board-top3__rating-value'}).get_text()
            templeaderboardrow.append(plyaersp)
            # 用户游戏场数
            playergametimes = item_top3.find('span',attrs={'class':'leader-board-top3__matches-cnt-value'}).get_text()
            templeaderboardrow.append(playergametimes)
            # 胜%
            temp = item_top3.find('i',attrs={'class':'sp__win'}).parent
            winpercent =re.search(r'\s+.*?\%',str(temp)).group(0).replace(' ','').replace('\n','')
            templeaderboardrow.append(winpercent)
            # top 10%
            temp = item_top3.find('i',attrs={'class':'sp__top10'}).parent
            playertop10percent =re.search(r'\s+.*?\%',str(temp)).group(0).replace(' ','').replace('\n','')
            templeaderboardrow.append(playertop10percent)
            #
            tempitem_top3_rest = item_top3.find_all('li',{'class':"leader-board-top3__info-item"})
            # K/D
            playerkd = tempitem_top3_rest[0].find_all('span')[1].get_text()
            templeaderboardrow.append(playerkd)
            # print(playerkd)
            # 伤害
            #
            playerdamage = tempitem_top3_rest[1].find_all('span')[1].get_text()
            templeaderboardrow.append(playerdamage)
            # print(playerdamage)
            # 平均排名
            playeravgrank = tempitem_top3_rest[5].find_all('span')[1].get_text()
            templeaderboardrow.append(playeravgrank)
            # print(playeravgrank)
            leaderboard.append(templeaderboardrow)
        play_rank_table = page.find('tbody').find_all('tr')
        for  i,item_tr in enumerate(play_rank_table):
            if(i<51):
                templeaderboardrow = []
                item_td = item_tr.find_all('td')
                #用户排名
                playerrank = item_td[0].find('span', attrs={'class': 'leader-board__number'}).get_text()
                templeaderboardrow.append(playerrank)
                # 用户id
                # print(i)
                playerid = item_td[1].find('a', attrs={'class': 'leader-board__nickname'}).get_text()
                templeaderboardrow.append(playerid)
                # print(playerid)
                # sp
                playersp = item_td[2].find('div', attrs={'class': 'leader-board__table-content '}).get_text()
                # print(playersp)
                templeaderboardrow.append(playersp)
                # 用户游戏场数
                playergametimes = item_td[3].find('div', attrs={'class': 'leader-board__table-content'}).get_text()
                # print(playergametimes)
                templeaderboardrow.append(playergametimes)
                # 胜%
                winpercent = item_td[4].find('span', attrs={'class': 'leader-board__grades-value'}).get_text()
                # print(winpercent)
                templeaderboardrow.append(winpercent)
                # top 10%
                playertop10percent = item_td[5].find('div', attrs={'class': 'leader-board__grades-value'}).get_text()
                # print(playertop10percent)
                templeaderboardrow.append(playertop10percent)
                # K/D
                playerkd = item_td[6].find('div', attrs={'class': 'leader-board__table-content'}).get_text().replace(
                    ' ', '').replace('\n', '')
                # print(playerkd)
                templeaderboardrow.append(playerkd)
                # 伤害
                playerdamage = item_td[7].find('div', attrs={'class': 'leader-board__grades-value'}).get_text().replace(
                    ' ', '').replace('\n', '')
                # print(playerdamage)
                templeaderboardrow.append(playerdamage)
                # 平均排名
                playeravgrank = item_td[8].find('div',
                                                attrs={'class': 'leader-board__table-content'}).get_text().replace(' ',
                                                                                                                   '').replace(
                    '\n', '')
                # print(playeravgrank)
                templeaderboardrow.append(playeravgrank)
                leaderboard.append(templeaderboardrow)
        print("start save")
        filename = 'simpleSpider_op_gg/spider_save_data/leaderboard-'+str(response.meta['mode'])+'-'+str(response.meta['teamsize'])+'.json'

        # with open('simpleSpider_op_gg/spider_save_data/','w') :
        # os.mknod(filename)
        with open(filename,'w') as file_object :
            json.dump(leaderboard,file_object)
        print("finish"+filename)