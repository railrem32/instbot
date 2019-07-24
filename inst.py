import random
from datetime import datetime
import requests
import db
from instapy import InstaPy
from instapy import smart_run
import config
import sys


enable_notifocation = True

def sendNotification(message,chat_id):
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text=".format(config.CONST_TOKEN, chat_id)+message
    requests.get(url)



class writer(object):
    log = ""
    file = open("log","w")
    def write(self, data):
        self.log = self.log + (data)

    def slush(self):
        self.file.write(self.log)



logger = writer()
sys.stdout = logger

def get_session(insta_username,insta_password):
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=True,
                      # nogui=True,
                      multi_logs=False,
                      disable_image_load=True)

    return session

# args:
# [0] = photos_grab_amount
# [1] = follow_likers_per_photo
#
def _follow_likers(session,user,args):
    session.follow_likers([user], photos_grab_amount=args[0], follow_likers_per_photo=args[1], randomize=False,
                          sleep_delay=600, interact=False)

def unfollow(task):
    user = task.get(db.FIELD_TARGET_USER)
    chat_id = task.get(db.FIELD_CHAT_ID)
    user_id = task.get(db.FIELD_USER_ID)

    setting = db.wrapUser(db.get_user_settings(user_id))
    insta_username = setting.get(db.FIELD_USERNAME)
    insta_password = setting.get(db.FIELD_PASSWORD)
    # Send notification to my Telegram

    if (enable_notifocation):
        message = "Начал обработку {} в {}".format(user, datetime.now().strftime("%H:%M:%S"))
        sendNotification(message, chat_id)

    # get a session!
    session = get_session(insta_username, insta_password)

    # let's go! :>
    with smart_run(session):
        # HEY HO LETS GO
        # general settings
        # session.set_dont_include(friends)
        # session.set_dont_like(dont_likes)
        # session.set_ignore_if_contains(ignore_list)
        # session.set_ignore_users(ignore_users)
        session.set_simulation(enabled=True)
        session.set_skip_users(skip_private=False,
                               private_percentage=100)


        # UNFOLLOW activity
        """ Unfollow all users followed by InstaPy after one week to keep the 
        following-level clean...
        """
        session.unfollow_users(amount=random.randint(75, 100),
                               InstapyFollowed=(True, "all"), style="FIFO",
                               unfollow_after=168 * 60 * 60, sleep_delay=600)

        """ Joining Engagement Pods...
        """
        session.join_pods()

    """
    Have fun while optimizing for your purposes, Nuzzo
    """

    # Send notification to my Telegram
    if (enable_notifocation):
        message = "Закончил обработку {} в {}".format(user, datetime.now().strftime("%H:%M:%S"))
        sendNotification(message, chat_id)


def follow_likers(task,photos,likers):
    user = task.get(db.FIELD_TARGET_USER)
    chat_id = task.get(db.FIELD_CHAT_ID)
    user_id = task.get(db.FIELD_USER_ID)

    setting = db.wrapUser(db.get_user_settings(user_id))
    insta_username = setting.get(db.FIELD_USERNAME)
    insta_password = setting.get(db.FIELD_PASSWORD)
    # Send notification to my Telegram

    if (enable_notifocation):
        message = "Начал обработку {} в {}".format(user, datetime.now().strftime("%H:%M:%S"))
        sendNotification(message, chat_id)

    # get a session!
    session = get_session(insta_username, insta_password)

    # let's go! :>
    with smart_run(session):
        # HEY HO LETS GO
        # general settings
        # session.set_dont_include(friends)
        # session.set_dont_like(dont_likes)
        # session.set_ignore_if_contains(ignore_list)
        # session.set_ignore_users(ignore_users)
        session.set_simulation(enabled=True)
        session.set_skip_users(skip_private=False,
                               private_percentage=100)

        session.set_relationship_bounds(enabled=True,
                                        potency_ratio=None,
                                        delimit_by_numbers=True,
                                        max_followers=15000,
                                        max_following=15000,
                                        min_followers=0,
                                        min_following=0,
                                        min_posts=0)

        session.set_user_interact(amount=1, randomize=True, percentage=80,
                                  media='Photo')
        session.set_do_like(enabled=True, percentage=90)
        # session.set_do_comment(enabled=True, percentage=15)
        # session.set_comments(comments, media='Photo')
        session.set_do_follow(enabled=True, percentage=99, times=1)

        session.set_quota_supervisor(enabled=True,
                                     sleep_after=["likes", "follows", "unfollows", "server_calls_h"],
                                     sleepyhead=True, stochastic_flow=True, notify_me=True,
                                     peak_likes=(57, 585),
                                     peak_follows=(56, 660),
                                     peak_unfollows=(49, 550),
                                     peak_server_calls=(490, None))

        """ Interact with the chosen targets...
        """
        session.follow_likers([user], photos_grab_amount=photos, follow_likers_per_photo=likers, randomize=False,
                              sleep_delay=600, interact=False)

        # UNFOLLOW activity
        """ Unfollow all users followed by InstaPy after one week to keep the 
        following-level clean...
        """
        # session.unfollow_users(amount=random.randint(75, 100),
        #                        InstapyFollowed=(True, "all"), style="FIFO",
        #                        unfollow_after=168 * 60 * 60, sleep_delay=600)

        """ Joining Engagement Pods...
        """
        session.join_pods()

    """
    Have fun while optimizing for your purposes, Nuzzo
    """

    # Send notification to my Telegram
    if (enable_notifocation):
        message = "Закончил обработку {} в {}".format(user, datetime.now().strftime("%H:%M:%S"))
        sendNotification(message, chat_id)

def follow_and_like(task):
    user = task.get(db.FIELD_TARGET_USER)
    chat_id = task.get(db.FIELD_CHAT_ID)
    user_id = task.get(db.FIELD_USER_ID)

    setting = db.wrapUser(db.get_user_settings(user_id))
    insta_username = setting.get(db.FIELD_USERNAME)
    insta_password =setting.get(db.FIELD_PASSWORD)
    # Send notification to my Telegram

    if (enable_notifocation):
        message = "Начал обработку {} в {}".format(user, datetime.now().strftime("%H:%M:%S"))
        sendNotification(message, chat_id)

    # get a session!
    session = get_session(insta_username, insta_password)

    # let's go! :>
    with smart_run(session):
        # HEY HO LETS GO
        session.set_simulation(enabled=True)
        session.set_skip_users(skip_private=False,
                               private_percentage=100)

        session.set_relationship_bounds(enabled=True,
                                        potency_ratio=None,
                                        delimit_by_numbers=True,
                                        max_followers=15000,
                                        max_following=15000,
                                        min_followers=0,
                                        min_following=0,
                                        min_posts=0)


        session.set_user_interact(amount=1, randomize=True, percentage=80,
                                  media='Photo')
        session.set_do_like(enabled=True, percentage=90)

        session.set_do_follow(enabled=True, percentage=99, times=1)

        session.set_quota_supervisor(enabled=True,
                                     sleep_after=["likes", "follows", "unfollows", "server_calls_h"],
                                     sleepyhead=True, stochastic_flow=True, notify_me=True,
                                     peak_likes=(57, 585),
                                     peak_follows=(56, 660),
                                     peak_unfollows=(49, 550),
                                     peak_server_calls=(490, None))



        """ Interact with the chosen targets...
        """
        followers = session.grab_followers(username=user, amount="full", live_match=True, store_locally=True)
        session.follow_by_list(followlist=followers, times=1, sleep_delay=600, interact=False)

        session.join_pods()

    # Send notification to my Telegram
    if (enable_notifocation) :
        message = "Закончил обработку {} в {}".format(user, datetime.now().strftime("%H:%M:%S"))
        sendNotification(message,chat_id)

