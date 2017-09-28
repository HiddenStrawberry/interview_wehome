import json

from Connection import Connection
import re
from ORM import *
import pandas as pd
import numpy as np
def get_location(html):
    location=re.findall('"lat":(.*?),"lng":(.*?),',html,re.S)[0]
    return {'lat':location[0],'lng':location[1]}
def get_roomer(html):
    return re.findall('"guest_label":"(.*?)"',html,re.S)[0]
def get_model(html):
    return re.findall('"localized_room_type":"(.*?)"',html,re.S)[0]
def get_apartment(html):
    return re.findall('"bedroom_label":"(.*?)"',html,re.S)[0]
def get_bed(html):
    return re.findall('"bed_label":"(.*?)"',html,re.S)[0]
def get_status(url):
    result={}
    cn=Connection.Connection()
    key='d306zoyjsyarp7ifhu67rjxn52tv0t20'
    html=cn.geturl('https://www.airbnbchina.cn/api/v2/calendar_months?key='+key+'&currency=CNY&locale=zh&listing_id='+url+'&month=9&year=2017&count=6&_format=with_conditions',needproxy=False)
    js=json.loads(html)
    month=js['calendar_months']
    for each in month:
        days=each['days']
        for each2 in days:
            result[each2['date']]=each2['available']
    return result

def analyze(result):
    date=[]
    available=[]
    for key,value in result.items():
        date.append(key)
        available.append(value)
    data={'date':date,'available':available}
    new = pd.DataFrame(data)
    new['available'].hist().get_figure().savefig('d:/plot.png')
    print new


if __name__=='__main__':
    cn=Connection.Connection()

    analyze(get_status('18509589'))
    # html=cn.geturl('http://www.airbnbchina.cn/rooms/18509589',needproxy=False)
    #
    # try:
    #     engine = create_engine(
    #         'mysql+mysqlconnector://cdb_outerroot:bydu88c3@590591aa5c333.sh.cdb.myqcloud.com:6107/stockproj')
    #     DBSession = sessionmaker(bind=engine)
    #     session = DBSession()
    #     try:
    #         session.add(wehome(room='18509589',
    #                             location=str(get_location(html)),
    #                             model=get_model(html),
    #                             roomer=get_roomer(html),
    #                             apartment=get_apartment(html),
    #                             bed=get_bed(html)))
    #         session.commit()
    #     except Exception as err:
    #         session.rollback()
    #         print err
    # except:
    #     pass
    # finally:
    #     session.close()

