#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
import urllib
import urllib2

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    title = Column(String, default=None)
    num_comments = Column(Integer, default=False)
    submitted = Column(Boolean, default=False)

    def __repr__(self):
        udecode = lambda x: x.encode("utf-8", "xmlcharrefreplace")
        sub_flag = "(S) " if self.submitted else ""
        return "<%sArticle: %s %s %d>" % (sub_flag, udecode(self.title), udecode(self.link), self.num_comments)

def make_session(dbfile, echo=False):
    engine = create_engine(dbfile, echo=echo)
    metadata = Base.metadata # from declarative base
    #metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class InstapaperAccount(object):

    def __init__(self, username, password=None):
        self.username = username
        self.password = password

    def add(self, article_obj):
        apiaddurl = "https://www.instapaper.com/api/add"

        # Encode parameters
        udecode = lambda x: x.encode("utf-8", "xmlcharrefreplace")
        params = {}
        params["username"] = self.username
        params["password"] = self.password
        params["url"] = udecode(article_obj.link)
        params["title"] = udecode(article_obj.title)
        data = urllib.urlencode(params)

        # Form request
        req = urllib2.Request(apiaddurl, data)
        resp = urllib2.urlopen(req)
        if resp.getcode() == 201:
            return True
        return False


def main():
    # Set up Instapaper
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.readfp(open('instapaper.ini'))
    ip = InstapaperAccount(config.get('login', 'username'),
                           config.get('login', 'password'))

    # Access Articles in sqlite
    session = make_session('sqlite:///articles.db')
    articles = session.query(Article).filter(Article.submitted == False)

    # Submit every article
    for article in articles:
        added = ip.add(article)
        if added:
            article.submitted = True
            print article
        else:
            print "SUBMIT FAILED:", article
        session.commit()

if __name__ == "__main__":
    main()
