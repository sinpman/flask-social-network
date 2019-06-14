from netflixpy import NetflixPy

netflix_email = ''
netflix_password = ''
netflix_profile = ''

# $x("//div[@class='galleryLockups']/div/div/div/div/div/div/div")
# 1500 movies
# 928 series
# 603 orignals
# = 3031
# @date 25th May 2018

session = NetflixPy(
    email=netflix_email,
    password=netflix_password,
    profile=netflix_profile,
    reload=True,
    lang='de-DE')

try:
    session.login()
    session.get_items('movies')

finally:
    # end the bot session
    session.end()
