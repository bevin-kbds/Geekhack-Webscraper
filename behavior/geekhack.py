import requests
from bs4 import BeautifulSoup

class MessageScraper:
    def __init__(self, url, file_name):
        self.base_url = url
        self.message_list = list()
        self.file_name = file_name
        with open(file_name) as id_file:
            lines = id_file.readlines()
            for line in lines:
                self.last_id = int(line.rstrip())
        self.id_list = [self.last_id]
    
    def update_ic(self):
        response = requests.get(self.base_url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        self.message_list.clear()
        for span in soup.find_all('span'):
            if span.get("id") is not None and int(span.get("id")[4:]) > self.last_id and span.text is not None and span.find('a')['href'] is not None:
                url = span.find('a')['href']
                self.id_list.append(int(span.get("id")[4:]))
                self.message_list.append((span.text, url, self.find_image(url), self.find_author(url), int(span.get("id")[4:])))
        self.message_list = sorted(self.message_list, key = (lambda x: x[4]))
    def update_post(self):
        response = requests.get(f'{self.base_url}#lastPost')
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        self.message_list.clear()
        for post in soup.find_all('div', attrs={'class':'postarea'}):
            last_post_id = int(post.find('h5', id = True).get('id')[8:])
            if self.last_id < last_post_id:
                self.id_list.append(last_post_id)
                last_post_url = post.find('a', href =True).get('href')
                timestamp = (post.find('div', attrs = {'class':'smalltext'}).text)
                title = post.find('a').text
                message = self.manage_quotes(post.find('div', attrs = {'class':'inner'}))
                self.message_list.append((title, last_post_url, timestamp, message))
    
    def manage_quotes(self, soup):
        headers=list()
        for message in soup.find_all('div', attrs={'class':"quoteheader"}):
            headers.append(message.text)
        for line_break in soup.find_all('br'):
            line_break.replace_with('\n')
        soup = BeautifulSoup(str(soup), 'html.parser')
        blockquotes = soup.find_all('blockquote', attrs={'class':"bbc_standard_quote"})
        main_message_list = list()
        for text in soup.find_all('div', attrs={'class' : 'inner'}):
            main_message_list.append(text.get_text())
        main_text = f''.join(main_message_list)
        if len(blockquotes) != 0:
            for blockquote in blockquotes:
                quotes = list(quote for blockquote in blockquotes for quote in blockquote.get_text('&&&&').split('&&&&') if not quote.startswith('Quote from:'))
            quote_depth = len(headers)-1
            quote_list = list()
            for index in reversed(range(len(headers))):
                quote_list.append(f'{"    "*index}**{headers[index]}**\n{"    "*index}{quotes[quote_depth - index].strip()}\n')
            return (quote_list, main_text)
        else:
            return (None, main_text)
            
            
                
            
        
    def find_image(self, url):
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        try:
            found_link = soup.find('div',attrs={"class":"inner"}).find('img')['src']
        except:
            return None
        return found_link

    
    def find_author(self, url):
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        found_name = soup.find('div',attrs={"class":"poster"}).find('a',href = True).text
        return found_name
    
    
    def repost_message(self):
        self.last_id = max(self.id_list)
        with open(self.file_name, 'w') as id_file:
            id_file.write(str(self.last_id))
        return self.message_list

if __name__ == '__main__':
    '''
    test = MessageScraper('https://geekhack.org/index.php?board=132.0', 'most_recent_IC_ID.txt')
    test2 = MessageScraper('https://geekhack.org/index.php?topic=115887.0', 'most_recent_post_ID.txt')
    test.update_ic()
    print(test.repost_message())
    test2.update_post()
    print(test2.repost_message())
    '''
    
    html_content = """
    <div class="inner" id="msg_3104456"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104332#msg3104332">Quote from: Keeblet_257 on Sun, 09 January 2022, 10:44:39</a></div></div><blockquote class="bbc_standard_quote">looks like a 500 units total GB and if this number gets splitup and region locked it basically means that EU will only get a maximum of 50-100 untis.<br />So getting this board is basically impossible D:<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br /><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104437#msg3104437">Quote from: moonmaster on Sun, 09 January 2022, 17:54:26</a></div></div><blockquote class="bbc_standard_quote">Color me interested. Any chance of doing an open quantity GB? Or something like 500 units or 750 unit max? <br /><br />Sent from my LE2125 using Tapatalk<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />I mentioned this in the IC but I chose a 35 unit count as this is the first group buy I am running and I don&#039;t want to bite off more than I can chew (I can already see 35 units being a daunting task to fulfill from a QC and shipping perspective). That said, I am closely monitoring the IC form and overall interest for the board. On the small chance that there is a need to increase unit count, albeit probably not to such high numbers like 500-750, I will reach out to vendors.</div>
    """
    #<div class="inner" id="msg_3105021"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104411#msg3104411">Quote from: kevinave on Sun, 09 January 2022, 15:47:37</a></div></div><blockquote class="bbc_standard_quote"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104406#msg3104406">Quote from: beelzking on Sun, 09 January 2022, 15:42:14</a></div></div><blockquote class="bbc_alternate_quote"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3103960#msg3103960">Quote from: Baka Bot on Fri, 07 January 2022, 11:47:16</a></div></div><blockquote class="bbc_standard_quote">I am not a fan of the engraving placement. But everything looks fine<br/></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div>this one. will there be an option to opt-out of the engraving part?<br/></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br/>With the current unit count, I doubt I would be able to provide an option to opt out of the top engraving. That said, if there is enough interest that I could increase unit count, I am not opposed to adding this as an option if there are no downsides.<br/></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br/>ic, no problem. This is a pretty good looking board and a pretty good IC for your first ever run, GLWIC.</div>

    content2 = """

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta name="verify-admitad" content="f9ec5b5de2" />
    <link rel="stylesheet" type="text/css" href="https://cdn.geekhack.org/Themes/Nostalgia/css/index.css?fin20" />
    <link rel="stylesheet" type="text/css" href="https://cdn.geekhack.org/Themes/default/css/webkit.css" />
    <script async src="https://www.googletagmanager.com/gtag/js"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'UA-26425837-1'); /* geekhack */
        gtag('config', 'UA-29278272-11', {
            linker: {
                domains: ['drop.com']
            }
        }); /* md */
    </script>
    
    <script type="text/javascript" src="https://cdn.geekhack.org/Themes/default/scripts/script.js?fin20"></script>
    <script type="text/javascript" src="https://cdn.geekhack.org/Themes/Nostalgia/scripts/theme.js?fin20"></script>
    <script type="text/javascript"><!-- // --><![CDATA[
        var smf_theme_url = "https://cdn.geekhack.org/Themes/Nostalgia";
        var smf_default_theme_url = "https://cdn.geekhack.org/Themes/default";
        var smf_images_url = "https://cdn.geekhack.org/Themes/Nostalgia/images";
        var smf_scripturl = "https://geekhack.org/index.php";
        var smf_iso_case_folding = false;
        var smf_charset = "ISO-8859-1";
        var ajax_notification_text = "Loading...";
        var ajax_notification_cancel_text = "Cancel";
    // ]]></script>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <meta name="description" content="[IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing" />
    <meta name="keywords" content="mechanical keyboard cherry MX buckling spring topre realforce filco razer switches geeky maker community phantom leopold vortex majestouch gaming typing enthusiasts hhkb happy hacking PFU fc700r fc500r fc200r 87u 104u ducky usb ps2 xt/at teensy arduino keycap otd kbdmania geekhack group buy" />
    <title>[IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</title>
    <link rel="canonical" href="https://geekhack.org/index.php?topic=115887.0" />
    <link rel="help" href="https://geekhack.org/index.php?action=help" />
    <link rel="search" href="https://geekhack.org/index.php?action=search" />
    <link rel="contents" href="https://geekhack.org/index.php" />
    <link rel="alternate" type="application/rss+xml" title="geekhack - RSS" href="https://geekhack.org/index.php?type=rss;action=.xml" />
    <link rel="prev" href="https://geekhack.org/index.php?topic=115887.0;prev_next=prev" />
    <link rel="next" href="https://geekhack.org/index.php?topic=115887.0;prev_next=next" />
    <link rel="index" href="https://geekhack.org/index.php?board=132.0" />
        <!-- App Indexing for Google Search -->
        <link href="android-app://com.quoord.tapatalkpro.activity/tapatalk/geekhack.org/?user_id=121512&amp;location=topic&amp;fid=132&amp;tid=115887&amp;perpage=50&amp;page=1&amp;channel=google-indexing" rel="alternate" />
        <link href="ios-app://307880732/tapatalk/geekhack.org/?user_id=121512&amp;location=topic&amp;fid=132&amp;tid=115887&amp;perpage=50&amp;page=1&amp;channel=google-indexing" rel="alternate" />
        
        <link href="https://groups.tapatalk-cdn.com/static/manifest/manifest.json" rel="manifest">
        
        <meta name="apple-itunes-app" content="app-id=307880732, affiliate-data=at=10lR7C, app-argument=tapatalk://geekhack.org/?user_id=121512&location=topic&fid=132&tid=115887&perpage=50&page=1" />
        
    <script type="text/javascript"><!-- // --><![CDATA[
        var _ohWidth = 480;
        var _ohHeight = 270;
    // ]]></script>
    <script type="text/javascript">!window.jQuery && document.write(unescape('%3Cscript src="//code.jquery.com/jquery-1.9.1.min.js"%3E%3C/script%3E'))</script>
    <script type="text/javascript" src="https://cdn.geekhack.org/Themes/default/scripts/ohyoutube.min.js"></script>
    <link rel="stylesheet" type="text/css" href="https://cdn.geekhack.org/Themes/default/css/oharaEmbed.css" /><script type="text/javascript" src="https://cdn.geekhack.org/Themes/default/scripts/ila.js"></script>
<link rel="stylesheet" href="https://cdn.geekhack.org/Themes/default/hs4smf/highslide.css" type="text/css" media="screen" />

<style type="text/css">    .highslide-wrapper, .highslide-outline {background: #FFFFFF;}</style>

    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script type="text/javascript" src="https://cdn.geekhack.org/Themes/default/scripts/more.js"></script>
    <script type="text/javascript" src="https://cdn.geekhack.org/Themes/default/scripts/image.js"></script>
</head>
<body>
<div id="wrapper" style="width: 95%">
    <div id="header"><div class="frame">
        <div id="top_section" style="background: url(https://geekhack.org/Themes/images/banner-bg-modelm-90.png
) no-repeat">
            <h1 class="forumtitle">
                <a href="https://geekhack.org/index.php"><img src="https://geekhack.org/Themes/Nostalgia/images/banner.png" alt="geekhack" /></a>
            </h1>
            <img id="upshrink" src="https://cdn.geekhack.org/Themes/Nostalgia/images/upshrink.png" alt="*" title="Shrink or expand the header." style="display: none;" />
            <div id="siteslogan" class="floatright">
                <form id="search_form" action="https://geekhack.org/index.php?action=search2" method="post" accept-charset="ISO-8859-1">
                    <input type="text" name="search" value="" class="input_text" />&nbsp;
                    <input type="submit" name="submit" value="Search" class="button_submit" />
                    <input type="hidden" name="advanced" value="1" />
                    <input type="hidden" name="topic" value="115887" />
                    <br><a class="news tighttext" href="https://geekhack.org/index.php?action=search;advanced" onclick="this.href += ';search=' + escape(document.forms.searchform.search.value);">Advanced search</a>
                </form>wanna switch?

            </div>
        </div>
        <div id="upper_section" class="middletext">
            <div class="user">
                <p class="avatar"><img src="https://geekhack.org/index.php?action=dlattach;attach=280838;type=avatar" alt="" class="avatar" /></p>
                <ul class="reset">
                    <li class="greeting">Hello <span>kevinave</span></li>
                    <li><a href="https://geekhack.org/index.php?action=recenttopics">Spy on the latest forum posts.</a></li>
                    <li><a href="https://geekhack.org/index.php?action=unread">Show unread topics since last visit.</a></li>
                    <li><a href="https://geekhack.org/index.php?action=unreadreplies">Show new replies to your posts.</a></li>
                    <li>Sun, 27 February 2022, 15:59:27</li>
                </ul>
            </div>
            <div class="news normaltext">
                <h2>News: </h2>
                <p>Have you read the <strong><a href="https://geekhack.org/index.php?topic=39249.0" class="bbc_link" target="_blank">geekhack TOS</a></strong> lately?</p>
            </div>
        </div>
        <br class="clear" />
        <script type="text/javascript"><!-- // --><![CDATA[
            var oMainHeaderToggle = new smc_Toggle({
                bToggleEnabled: true,
                bCurrentlyCollapsed: false,
                aSwappableContainers: [
                    'upper_section'
                ],
                aSwapImages: [
                    {
                        sId: 'upshrink',
                        srcExpanded: smf_images_url + '/upshrink.png',
                        altExpanded: 'Shrink or expand the header.',
                        srcCollapsed: smf_images_url + '/upshrink2.png',
                        altCollapsed: 'Shrink or expand the header.'
                    }
                ],
                oThemeOptions: {
                    bUseThemeSettings: true,
                    sOptionName: 'collapse_header',
                    sSessionVar: 'b1b588e33',
                    sSessionId: '749de156f0789523e77cbbc9ade2366d'
                },
                oCookieOptions: {
                    bUseCookie: false,
                    sCookieName: 'upshrink'
                }
            });
        // ]]></script>
        <div id="main_menu">
            <ul class="dropmenu" id="menu_nav">
                <li id="button_home">
                    <a class="firstlevel active firstlevel" href="https://geekhack.org/index.php">
                        <span class="firstlevel">Home</span>
                    </a>
                </li>
                <li id="button_watched">
                    <a class="firstlevel firstlevel" href="https://geekhack.org/index.php?action=watched">
                        <span class="firstlevel">Watched</span>
                    </a>
                </li>
                <li id="button_unread">
                    <a class="firstlevel firstlevel" href="https://geekhack.org/index.php?action=unread">
                        <span class="firstlevel">Unread</span>
                    </a>
                </li>
                <li id="button_notifications">
                    <a class="firstlevel firstlevel" href="https://geekhack.org/index.php?action=profile;area=notification">
                        <span class="firstlevel">Notifications</span>
                    </a>
                </li>
                <li id="button_irc">
                    <a class="firstlevel firstlevel" href="http://webchat.freenode.net/?channels=geekhack">
                        <span class="firstlevel">IRC</span>
                    </a>
                </li>
                <li id="button_wiki">
                    <a class="firstlevel firstlevel" href="http://wiki.geekhack.org">
                        <span class="firstlevel">Wiki</span>
                    </a>
                </li>
                <li id="button_search">
                    <a class="firstlevel firstlevel" href="https://geekhack.org/index.php?action=search">
                        <span class="firstlevel">Search</span>
                    </a>
                </li>
                <li id="button_profile">
                    <a class="firstlevel firstlevel" href="https://geekhack.org/index.php?action=profile">
                        <span class="firstlevel">Profile</span>
                    </a>
                    <ul>
                        <li>
                            <a href="https://geekhack.org/index.php?action=profile">
                                <span>Summary</span>
                            </a>
                        </li>
                        <li>
                            <a href="https://geekhack.org/index.php?action=profile;area=showposts">
                                <span>Show Posts</span>
                            </a>
                        </li>
                        <li>
                            <a href="https://geekhack.org/index.php?action=profile;area=account">
                                <span>Account Settings</span>
                            </a>
                        </li>
                        <li>
                            <a href="https://geekhack.org/index.php?action=profile;area=forumprofile">
                                <span>Forum Profile</span>
                            </a>
                        </li>
                        <li>
                            <a href="https://geekhack.org/index.php?action=profile;area=notification">
                                <span class="last">Notifications</span>
                            </a>
                        </li>
                    </ul>
                </li>
                <li id="button_pm">
                    <a class="firstlevel firstlevel" href="https://geekhack.org/index.php?action=pm">
                        <span class="firstlevel">Messages</span>
                    </a>
                    <ul>
                        <li>
                            <a href="https://geekhack.org/index.php?action=pm">
                                <span>Read your messages</span>
                            </a>
                        </li>
                        <li>
                            <a href="https://geekhack.org/index.php?action=pm;sa=send">
                                <span class="last">Send a message</span>
                            </a>
                        </li>
                    </ul>
                </li>
                <li id="button_recenttopics">
                    <a class="firstlevel firstlevel" href="https://geekhack.org/index.php?action=recenttopics">
                        <span class="firstlevel">Spy</span>
                    </a>
                </li>
                <li id="button_logout">
                    <a class="last firstlevel firstlevel" href="https://geekhack.org/index.php?action=logout;b1b588e33=749de156f0789523e77cbbc9ade2366d">
                        <span class="last firstlevel">Logout</span>
                    </a>
                </li>
            </ul>
        </div>
        <br class="clear" />
    </div></div>
    <div id="content_section"><div class="frame">
        <div id="main_content_section">
    <div class="navigate_section">
        <ul>
            <li>
                <a href="https://geekhack.org/index.php"><span>geekhack</span></a> &#187;
            </li>
            <li>
                <a href="https://geekhack.org/index.php#c49"><span>geekhack Marketplace</span></a> &#187;
            </li>
            <li>
                <a href="https://geekhack.org/index.php?board=132.0"><span>Interest Checks</span></a> (Moderator: <a href="https://geekhack.org/index.php?action=profile;u=31271" title="Board Moderator">Signature</a>) &#187;
            </li>
            <li class="last">
                <a href="https://geekhack.org/index.php?topic=115887.0"><span>[IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</span></a>
            </li>
        </ul>
    </div>
            <a id="top"></a>
            <a id="msg3103950"></a>
            <div class="pagesection">
                <div class="nextlinks"><a href="https://geekhack.org/index.php?topic=115887.0;prev_next=prev#new">&laquo; previous</a> <a href="https://geekhack.org/index.php?topic=115887.0;prev_next=next#new">next &raquo;</a></div>
        <div class="buttonlist floatright">
            <ul>
                <li><a class="button_strip_reply active" href="https://geekhack.org/index.php?action=post;topic=115887.0;last_msg=3113180"><span>Reply</span></a></li>
                <li><a class="button_strip_watch" href="https://geekhack.org/index.php?action=unwatch;topic=115887.0;b1b588e33=749de156f0789523e77cbbc9ade2366d"><span>Unwatch</span></a></li>
                <li><a class="button_strip_notify" href="https://geekhack.org/index.php?action=notify;sa=off;topic=115887.0;b1b588e33=749de156f0789523e77cbbc9ade2366d" onclick="return confirm('Are you sure you wish to disable notification of new replies for this topic?');"><span>Unnotify</span></a></li>
                <li><a class="button_strip_mark_unread" href="https://geekhack.org/index.php?action=markasread;sa=topic;t=3113185;topic=115887.0;b1b588e33=749de156f0789523e77cbbc9ade2366d"><span>Mark unread</span></a></li>
                <li><a class="button_strip_send" href="https://geekhack.org/index.php?action=emailuser;sa=sendtopic;topic=115887.0"><span>Send this topic</span></a></li>
                <li><a class="button_strip_print" href="https://geekhack.org/index.php?action=printpage;topic=115887.0" rel="new_win nofollow"><span class="last">Print</span></a></li>
            </ul>
        </div>
                <div class="pagelinks floatleft">Pages: &nbsp;[<strong>1</strong>] &nbsp;  &nbsp;&nbsp;<a href="#lastPost"><strong>Go Down</strong></a></div>
            </div>
            <div id="forumposts">
                <div class="cat_bar">
                    <h3 class="catbg">
                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/topic/hot_post.gif" align="bottom" alt="" />
                        <span id="author">Author</span>
                        Topic: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing &nbsp;(Read 10220 times)
                    </h3>
                </div>
                <p id="whoisviewing" class="smalltext"><a href="https://geekhack.org/index.php?action=profile;u=121512">kevinave</a> and 0 Guests are viewing this topic.
                </p>
                <form action="https://geekhack.org/index.php?action=quickmod2;topic=115887.0" method="post" accept-charset="ISO-8859-1" name="quickModForm" id="quickModForm" style="margin: 0;" onsubmit="return oQuickModify.bInEditMode ? oQuickModify.modifySave('749de156f0789523e77cbbc9ade2366d', 'b1b588e33') : false">
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Online"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useron.gif" alt="Online" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=121512" title="View the profile of kevinave">kevinave</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3103950_extra_info">
                                <li class="stars"></li>
                                <li class="threadstarter">
                                    <b>Thread Starter</b>
                                </li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=121512">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280838;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 19</li><li class="blurb">Location: California</li>
                                <li class="blurb">keebing it cool</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=121512"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3103950" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Personal Message (Online)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_on.gif" alt="Personal Message (Online)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" id="msg_icon_3103950" />
                                    </div>
                                    <h5 id="subject_3103950">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3103950#msg3103950" rel="nofollow">[IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong> on:</strong> Fri, 07 January 2022, 11:21:09 &#187;</div>
                                    <div id="msg_3103950_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3103950;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3103950);">Quote</a></li>
                                    <li class="mquote" id="mquote_3103950"><a href="javascript:void(0);" onclick="return mquote(3103950,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3103950"><a href="javascript:void(0);" onclick="return mquote(3103950,'remove');">Multi-Quote</a></li>
                                    <li class="modify_button"><a href="https://geekhack.org/index.php?action=post;msg=3103950;topic=115887.0">Modify</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3103950"><hr /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-family: courier;" class="bbc_font"><span style="font-size: 18pt;" class="bbc_size">Calla</span></span></span><br /><br /><hr /><br /><a  href="http://i.imgur.com/FJhwrfn.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/FJhwrfn.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><a  href="http://i.imgur.com/puHn0zH.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/puHn0zH.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><a  href="http://i.imgur.com/F0pbCMx.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/F0pbCMx.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><br /><hr /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Directory:</strong></span></span></span><br /><ul class="bbc_list"><li><a href="https://discord.gg/yNUPenF59g" class="bbc_link" target="_blank"><strong>Discord</strong></a></li><li><a href="https://forms.gle/f4xJijkZSnkqedQ38" class="bbc_link" target="_blank"><strong>Interest Check Response Form</strong></a></li><li><a href="https://docs.google.com/spreadsheets/d/1dD4QSbrBYBxJfmBSrPmv0h0tP35393vytqnkWBa45fE/edit?usp=sharing" class="bbc_link" target="_blank"><strong>Interest Check Q&amp;A Document, Keycap Compatibility, Screw Kit</strong></a></li><li><a href="https://imgur.com/a/TuLRjXE" class="bbc_link" target="_blank"><strong>Render album</strong></a> (as always, there will inevitably be differences in renders and real anodization colors)</li><li><a href="https://imgur.com/a/xbglcaR" class="bbc_link" target="_blank"><strong>V1 Prototype album</strong></a></li><li><a href="https://youtu.be/VnOIbJmiz0A" class="bbc_link" target="_blank"><strong>Prototype V1 Soundtest (youtube)</strong></a> <br /></li></ul><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Group buy:</strong></span></span></span><br /><ul class="bbc_list"><li>Q2 2022 group buy date. (Date and details will be finalized shortly after receiving the second prototype)</li><li>Fixed WKL kits</li><li>35 unit FCFS</li><li>5 additional units FNF</li><li>x units reserved for order replacements and extras</li><li>Target cost of $500 but potential price increases by GB</li></ul><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Summary:</strong></span></span></span><br /><ul class="bbc_list"><li>Seamless Side Profile F13 WKL TKL</li><li>Top mount or O-ring gummy ring gasket mount</li><li>18.9 mm switch spacing</li><li>5.5 typing angle</li><li>21.9 mm effective keyboard height / 17.9 mm front face height (w/o bumpers)</li><li>QMK and VIA driven PCB compatible with both MX and Alps switches (Alps compatible plates will not be offered in the group buy; however, I will provide files for Alp compatible plates shortly before the fulfillment date)</li><li>Top engraving featuring a Calla lily</li><li>Stainless steel internal and external weights centered around the alphas</li><li>Flush M3 case hex screws for easy assembly and disassembly</li><li>Universal daughterboard situated parallel to the surface of the table and aligned between the nav cluster and alphas.</li><li>Pricing is not finalized, targetting $500 USD</li></ul><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Roadmap:</strong></span></span></span><br /><ul class="bbc_list"><li>Order first prototype: <span style="color: yellow;" class="bbc_color"><strong>Completed</strong></span></li><li>Evaluate first prototype: <span style="color: yellow;" class="bbc_color"><strong>Completed</strong></span></li><li>Post IC: <span style="color: yellow;" class="bbc_color"><strong>Completed</strong></span></li><li>IC feedback stage: <span style="color: red;" class="bbc_color"><strong>Here</strong></span></li><li>Order second prototype:</li><li>Evaluate second prototype:</li><li>Group Buy:</li></ul><br /><hr /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Background Info:</strong></span></span></span><br />Yes, it is another F13 TKL; however, rather than the standard cherry specification of 19.05 mm used in most keyboards, Calla features a reduced switch spacing of 18.9 mm.<br /><br />I was inspired by the coveted OTD mini, one of the first boards to feature a switch spacing that deviated from the standard 19.05 mm. Researching more about the OTD mini led to me designing my own board that not only modifies the switch spacing but also negates the inconsistencies that occur with lower switch spacings. With this, Calla is around 2.7 mm shorter than the standard TKL using stock cherry spacing [18u(19.05 mm - 18.9 mm)/1u = ~2.7 mm] when comparing keycaps.<br /><br /><a  href="http://i.imgur.com/IodmoLT.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/IodmoLT.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><br /><a  href="http://i.imgur.com/Gaz02vs.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/Gaz02vs.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><br /><hr /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Color Options</strong></span></span></span><br /><br />Please vote for your favorite colors in the <a href="https://forms.gle/f4xJijkZSnkqedQ38" class="bbc_link" target="_blank">IC form</a> as I will be reducing the number of colors available based on popularity. <br /><br /><a  href="http://i.imgur.com/6mebIXB.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/6mebIXB.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><br /><div class="more_head">More</div><div class="more_body"><a  href="http://i.imgur.com/yE64KkH.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/yE64KkH.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><a  href="http://i.imgur.com/QzGgLJW.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/QzGgLJW.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><a  href="http://i.imgur.com/NalF4qq.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/NalF4qq.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><a  href="http://i.imgur.com/LySLaOX.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/LySLaOX.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><a  href="http://i.imgur.com/jZ3BBDl.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/jZ3BBDl.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a></div><br /><span style="font-size: 8pt;" class="bbc_size"><em>*As always these are only renders. Color display variations, manufacturer capabilities, and real-life lighting will all inevitably lead to differences in the final product.</em></span><br /><br /><hr /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Group buy kit:</strong></span></span></span><br /><ul class="bbc_list"><li>1 x Top Case (6063 aluminum)</li><li>1 x Bottom Case (6063 aluminum)</li><li>1 x Interior Weight (304 stainless steel [potentially brass if the second prototype is promising])</li><li>1 x Exterior Weight (304 stainless steel)</li><li>1 x Aluminum Plate (5052 aluminum: anodized red/silver/black depending on results of IC)</li><li><strong>Screw Kit</strong> sourced from McMaster and packed by me <em>(kit is subject to change upon receiving the second prototype)</em>:</li><ul class="bbc_list"><li>8x M3 8mm 18-8 SS Steel Socket Head Case screws <strong>(91292A112)</strong></li><li>2x M3 4mm 18-8 SS Hex Drive Flat Head Weight Screws <strong>(92125A127)</strong></li><li>7x M2.5 6mm 18-8 SS Steel Socket Head Plate Screws <strong>(91292A010)</strong></li><li>4x M2 3mm 18-8 SS Steel Socket Head Daughterboard Screws <strong>(91292A003)</strong></li></ul><li>1 x Clear Gummy O-ring (30A or 50A, depending on IC)</li><li>1 x Calla Solder PCB</li><li>1 x 100 mm JST connector</li><li>1 x Universal Daughterboard</li><li>4 x Keyboard bumpons</li></ul><br /><a  href="http://i.imgur.com/fjl8axi.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/fjl8axi.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><br /><a  href="http://i.imgur.com/iBWpl0F.png" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/iBWpl0F.png" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><br /><hr /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Planned Extras:</strong></span></span></span><br /><ul class="bbc_list"><li>Calla PCBs and Daughterboards</li><li>O-rings (both 30A and 50A)</li><li>(depending on IC) Plates</li><li>laser cut thin PE plate foam</li></ul><br /><a  href="http://i.imgur.com/Qc2CnMj.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103950' })"><img src="http://i.imgur.com/Qc2CnMj.jpg" alt="" width="640" height="360" align="" class="bbc_img" /></a><br /><br /><hr /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>A little about the planned group buy experience:</strong></span></span></span><br /><br />It is important to note (if you haven’t already) that this will be the first group buy I will have run; however, I will say that I am no stranger to the group buy process and that I am fully committed to providing a stress-free and easy group buy experience through frequent updates once the group buy has begun.<br /><br />Currently, I plan on a FCFS format sometime in Q2 2022. For the amount of interest I expect to receive, the number of units should be enough to cover most if not all participants who are interested in the board.<br /><br />After the purchasing window of the group buy, I intend to at least provide updates every other week if my health allows it. I hate feeling left in the dark about the inner workings of a group buy and I hope to be as transparent as possible to alleviate such worries. I plan on providing the same updates on both the GeekHack GB page and my discord server to make updates as accessible as possible.<br /><br />Lastly, for the group buy participants, I plan on running annual PCB group buys as I recognize that there are currently no other PCBs that are compatible with Calla.<br /><br /><hr /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Q&amp;A:</strong></span></span></span><br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 12pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>How is the bottom row keycap spacing retained while using the lower switch spacing?</strong></span></span></span><br />I adjusted the bottom row to negate the extra length of a standard 7u spacebar when compared to the nominal length of a 7u spacebar with 18.9 mm as the switch spacing (only possible with a fixed WKL layout). The left and right alt keys are ever so slightly offset away from the spacebar to account for the lower switch spacing.<br /><br /><span style="color: yellow;" class="bbc_color"><strong>Sadly, I can only offer WKL kits as it is not physically possible to implement WK with this design decision.</strong></span><br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 12pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Why Calla?</strong></span></span></span><br />Calla lilies have always been my favorite flower and they encapsulate the subtle curves of the board.<br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 12pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>What is engraved on the interior weight?</strong></span></span></span><br />The engraving on the interior weight reads &quot;in bloom again,&quot; and was taken from the quote &quot;The calla lilies are in bloom again.&quot;<br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 12pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Alps compatible PCB but no Alps compatible plate?</strong></span></span></span><br />I do not plan on offering Alps compatible plates during the GB but I will release Alps plate files for whoever wants them.<br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 12pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>NE iso support avail?</strong></span></span></span><br />Currently, I do not plan on supporting ISO layouts. The lower switch spacing leads to awkward ISO compatibility.<br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 12pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>NE plate foam avail?</strong></span></span></span><br />I had designed the board without foam in mind; however, I do understand that people appreciate the adjustability and sound that foam provides. Thus, PE plate foam is avail as extra. (just for you aka)<br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 12pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Pricing?</strong></span></span></span><br />I&#039;ve been getting this question a lot and I felt the need the address this. I am targetting a base cost of $500 before shipping. However, with the low unit count and changing metal/international shipping prices, the quotes I have received have been fluctuating sporadically and it is difficult to know if my target price will hold by the group buy date. Also, I do not want to promise one price during IC but sell at a higher one out of necessity during the GB. I have been holding off from providing a concrete price for these reasons, but have come to realize that it may be better to provide at least a loose target price so people may plan accordingly in this sea of group buys. By the second prototype, I will try to have a more concrete unit cost.<br /><br />So, TLDR: Target price of $500 USD before shipping, but price increases of up to 15% is possible due to the low volume/processing and QC costs/fluctuating metal and shipping prices/global pandemic.<br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-family: courier;" class="bbc_font"><span style="font-size: 12pt;" class="bbc_size"><strong>Will there be more units?</strong></span></span></span><br />This will be my first time running a group buy and I do not want to fall into the trap of ‘unlimited’ group buys that take years to fulfill. If there is an unexpectedly large amount of interest compared to the planned number of units, I may raise the unit count and reach out to vendors to process the extra units.<br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 12pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Vendors?</strong></span></span></span><br />If interest for the board far exceeds my expectations such that the planned number of units is far below the number of people who intend to purchase a unit, I may increase the unit count and seek out vendors. <br />I feel that the current number of units is adequate for the amount of interest I expect to receive and that I can QC and process the current number of units by myself.<br /><br /><hr /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Afterword:</strong></span></span></span><br /><br />If you’ve read it this far into my IC or had just instantly skipped to the end, I want to sincerely thank you. Just being able to share my project with you has been a rewarding experience and I have been able to meet so many wonderful people throughout the process to get here. Thus, I want to thank you for your interest and I hope that I was able to convince you to stay around a bit (even if it was to spam emotes).<br /><br />A little about myself: My name is Kevin and I am a college student who probably spends an unhealthy amount of time messing with switches and keyboards. Designing and building even the smallest things has always brought me joy and was what led to everything you see on this page being made or designed by me. Although I began this project by myself, I am confident that I will be able to bring a unique and competent board to you. </div>
                            </div>
                            <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/modify_inline.gif" alt="Modify message" title="Modify message" class="modifybutton" id="modify_button_3103950" style="cursor: pointer; display: none;" onclick="oQuickModify.modifyMsg('3103950')" />
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3103950">
                                &#171; <em>Last Edit: Sun, 27 February 2022, 03:27:49 by kevinave</em> &#187;
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.0;msg=3103950">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">136.52.119.125</a>
                            </div>
                            <div class="signature" id="msg_3103950_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3103951"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Online"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useron.gif" alt="Online" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=121512" title="View the profile of kevinave">kevinave</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3103951_extra_info">
                                <li class="stars"></li>
                                <li class="threadstarter">
                                    <b>Thread Starter</b>
                                </li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=121512">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280838;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 19</li><li class="blurb">Location: California</li>
                                <li class="blurb">keebing it cool</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=121512"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3103951" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Personal Message (Online)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_on.gif" alt="Personal Message (Online)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" id="msg_icon_3103951" />
                                    </div>
                                    <h5 id="subject_3103951">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3103951#msg3103951" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #1 on:</strong> Fri, 07 January 2022, 11:21:39 &#187;</div>
                                    <div id="msg_3103951_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3103951;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3103951);">Quote</a></li>
                                    <li class="mquote" id="mquote_3103951"><a href="javascript:void(0);" onclick="return mquote(3103951,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3103951"><a href="javascript:void(0);" onclick="return mquote(3103951,'remove');">Multi-Quote</a></li>
                                    <li class="modify_button"><a href="https://geekhack.org/index.php?action=post;msg=3103951;topic=115887.0">Modify</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3103951"><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Prototype V1:</strong></span></span></span><br /><br /><a href="https://imgur.com/nCiUIT6" class="bbc_link" target="_blank"><img src="http://i.imgur.com/nCiUIT6.jpg" alt="" width="640" height="480" align="" class="bbc_img" /></a><br /><ul class="bbc_list"><li><a href="https://imgur.com/a/xbglcaR" class="bbc_link" target="_blank"><strong>Prototype V1 album</strong></a></li><li><a href="https://youtu.be/VnOIbJmiz0A" class="bbc_link" target="_blank"><strong>Prototype V1 Soundtest (youtube)</strong></a> (Alu full plate with L+F HG blacks top mounted)</li></ul><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 14pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>My thoughts on this prototype: </strong></span></span></span><br /><ul class="bbc_list"><li>Mounting points are rather stiff as the norm with top-mounted boards, I&#039;m implementing a slight relief cut near the mounting points to alleviate this in future boards as well as moving the mounting points slightly for a more consistent alpha typing feel. </li><li>Keycap to keycap spacing and keycap to wall spacing is near perfect and looks amazing. </li><li>Manu quality is... not ideal. My worst fears were realized and I am not satisfied with how my order was handled and the overall quality of the anodization. There are some visible streaks on the bottom piece of the prototype and visible machining marks both inside and outside of the case. I am currently looking for a new manufacturer and have narrowed it down to two potential manufacturers for the second round of prototypes. </li><li>Overall, I am happy that everything works, the board sounds good, doesn&#039;t need foam, and both top mount/o-ring configurations work (albeit I ordered the wrong sizes of o-rings).</li></ul><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 14pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Running list of things changing in the second prototype: </strong></span></span></span><br /><ul class="bbc_list"><li>This section is dedicated to changes occurring during the second prototype phase. A change made here may or may not make it to the group buy version of the board.</li></ul><div class="more_head">More</div><div class="more_body"><ul class="bbc_list"><li>New case manufacturer.</li><li>Brass interior weight instead of stainless steel interior weight (to test the claim that brass interior weights produce a more ‘full’ sound compared to steel interior weights). This does not necessarily mean I will be changing the interior weight from steel to brass during the group buy.</li><li>Redesigned mounting points to reduce stiffness near said points.</li><li>Slightly reduced interior space. </li><li>Changed M2 to M3 screws (why I used M2 for the first prototype I do not know). </li><li>Adjusted bottom top-mounted screw locations for a more consistent R1-R2 typing experience.</li><li>Distributed weight screws more evenly as well as expanded interior weight.</li><li>misc. PCB improvements</li><li>Enlarged USB port to better accommodate different cables (01/09/2022)</li><li>Enlarged back &quot;Calla&quot; engraving slightly (01/09/2022)</li><li>Redistributed case screws. A side affect of changing M2 to M3 Screws that flew under my radar (01/10/2022)</li><li>Changed plate screws to M2.5, just to add a bit of vitality to the screws and threads (01/10/2022)</li><li>Added clearance underneath the plate screws so those that wish burger mount may do so (01/10/2022)</li></ul></div><br />With enough luck, I should be able to order a second prototype shortly after receiving feedback from this IC.<br /><br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 16pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>Keycap Compatibility:</strong></span></span></span><br /><ul class="bbc_list"><li>This section is dedicated to different keycap profiles and different keycap manufacturers being mounted onto Calla as a means to verify compatibility.</li></ul><div class="more_head">More</div><div class="more_body"><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 14pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>EPBT Cherry profile:</strong></span></span></span><br /><a  href="https://i.imgur.com/n8rG6kT.jpg?1" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103951' })"><img src="https://i.imgur.com/n8rG6kT.jpg?1" alt="" width="640" height="480" align="" class="bbc_img" /></a><br /><ul class="bbc_list"><li><a href="https://drive.google.com/file/d/1TQqa4spwaIwO_jpKwCdVs1orO0KlGrc2/view?usp=sharing" class="bbc_link" target="_blank"><strong>Soundtest</strong></a></li></ul><br />These are EPBT Black Japanese used in the prototype album. Standard keycap puller fits between the keycap-keycap and keycap-wall gaps. For keys like F13 and ESC, there was some difficulty fitting the puller but I was able to remove the keycaps without having to disassemble the case.<br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 14pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>KAT profile:</strong></span></span></span><br /><a  href="https://i.imgur.com/C2THde3.jpg?1" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103951' })"><img src="https://i.imgur.com/C2THde3.jpg?1" alt="" width="640" height="480" align="" class="bbc_img" /></a><br /><ul class="bbc_list"><li><a href="https://drive.google.com/file/d/1Shgv80mwvltkGalFUdRXE95VR6_6-5If/view?usp=sharing" class="bbc_link" target="_blank"><strong>Soundtest</strong></a></li></ul><br />These are Kitty KAT keycaps designed by Minterly Studios. I had to use an EPBT spacebar due to a common issue with 7u KAT spacebars at the time that causes it to not return. Standard keycap puller fits between the keycap-keycap and keycap-wall gaps. For keys like F13 and ESC, there was some difficulty fitting the puller but I was able to remove the keycaps without having to disassemble the case. On HG Cherry blacks, if I intentionally squeeze two adjacent keycaps together, they will make light contact. However, this is a fringe case and would never happen during normal use.<br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 14pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>MT3 profile:</strong></span></span></span><br /><a  href="https://i.imgur.com/1geVOA3.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103951' })"><img src="https://i.imgur.com/1geVOA3.jpg" alt="" width="640" height="480" align="" class="bbc_img" /></a><br /><ul class="bbc_list"><li><a href="https://drive.google.com/file/d/1uutrv3YKpnt2PVFgTW9SKdlmbJTl7C5q/view?usp=sharing" class="bbc_link" target="_blank"><strong>Soundtest</strong></a></li></ul><br />These are DROP + Mito MT3 Cyber keycaps. Standard keycap puller fits between the keycap-keycap and keycap-wall gaps, much tighter than the EPBT cherry. For keys like F13, ESC, control/alt, and the upper arrow key, there was some difficulty fitting the puller but I was able to remove the keycaps without having to disassemble the case. On HG Cherry blacks, if I intentionally squeeze two adjacent keycaps together, they will make light contact. However, this is a fringe case and would never happen during normal use. Keys were more difficult to remove but I was again able to remove all keycaps without disassembling the case. For MT3 users though, I would recommend disassembling the case to change keycaps.<br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 14pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>SP SA-P profile:</strong></span></span></span><br /><a  href="https://i.imgur.com/TR2E0N5.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103951' })"><img src="https://i.imgur.com/TR2E0N5.jpg" alt="" width="640" height="480" align="" class="bbc_img" /></a><br /><br />These are SP SA-P Snow Caps. Standard keycap puller fits between the keycap-keycap and keycap-wall gaps, slightly tighter than the EPBT cherry. For keys like F13, ESC, control/alt, and the upper arrow key, there was some difficulty fitting the puller but I was able to remove the keycaps without having to disassemble the case. On HG Cherry blacks, if I intentionally squeeze two adjacent keycaps together, they come close but do not make contact. I was again able to remove all keycaps without disassembling the case.<br /><br /><span style="color: floralwhite;" class="bbc_color"><span style="font-size: 14pt;" class="bbc_size"><span style="font-family: courier;" class="bbc_font"><strong>GMK Cherry profile:</strong></span></span></span><br /><a  href="https://i.imgur.com/hzmgxjj.jpg" class="highslide " onclick="return hs.expand(this, { slideshowGroup: '3103951' })"><img src="https://i.imgur.com/hzmgxjj.jpg" alt="" width="640" height="480" align="" class="bbc_img" /></a><br /><br />These are GMK Modern Dolch 2 Mist. I only mounted the necessary keycaps for this section. Standard keycap puller fits between the keycap-keycap and keycap-wall gaps, very similar to EPBT cherry. For keys like F13, ESC, control/alt, and the upper arrow key, there was not too much difficulty fitting the puller and I was able to remove the keycaps without having to disassemble the case. On HG Cherry blacks, if I intentionally squeeze two adjacent keycaps together, they come close but do not make contact. I was again able to remove all keycaps without disassembling the case.<br /><br /></div><br /><em>Special thanks to K105ty for letting me borrow their SA and GMK keycaps!</em></div>
                            </div>
                            <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/modify_inline.gif" alt="Modify message" title="Modify message" class="modifybutton" id="modify_button_3103951" style="cursor: pointer; display: none;" onclick="oQuickModify.modifyMsg('3103951')" />
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3103951">
                                &#171; <em>Last Edit: Sun, 13 February 2022, 01:35:41 by kevinave</em> &#187;
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.1;msg=3103951">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">136.52.119.125</a>
                            </div>
                            <div class="signature" id="msg_3103951_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3103952"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=126447" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=126447" title="View the profile of shima">shima</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3103952_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=126447">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=279071;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 63</li><li class="blurb">Location: California</li>
                                <li class="blurb">keeb weeb</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=126447"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=126447" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3103952">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3103952#msg3103952" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #2 on:</strong> Fri, 07 January 2022, 11:25:53 &#187;</div>
                                    <div id="msg_3103952_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3103952;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3103952);">Quote</a></li>
                                    <li class="mquote" id="mquote_3103952"><a href="javascript:void(0);" onclick="return mquote(3103952,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3103952"><a href="javascript:void(0);" onclick="return mquote(3103952,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3103952">calla so lit <img src="https://cdn.geekhack.org/Smileys/solosmileys/cool.gif" alt="&#58;cool&#58;" title="cool" class="smiley" /></div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3103952">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.2;msg=3103952">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3103952_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a><a href="https://geekhack.org/index.php?topic=116187.0" class="bbc_link" target="_blank"><img src="https://imgur.com/uqxW4c9.png" alt="" width="288" height="120" align="" class="bbc_img resized" /></a><br /><br />Palette G67 | Kyuu | Biscutneko | F1-8X</div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3103954"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=147463" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=147463" title="View the profile of brudder">brudder</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3103954_extra_info">
                                <li class="stars"></li>
                                <li class="postcount">Posts: 7</li>
                                <li class="blurb">youtube.com/brudder</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=147463"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=147463" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3103954">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3103954#msg3103954" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #3 on:</strong> Fri, 07 January 2022, 11:30:53 &#187;</div>
                                    <div id="msg_3103954_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3103954;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3103954);">Quote</a></li>
                                    <li class="mquote" id="mquote_3103954"><a href="javascript:void(0);" onclick="return mquote(3103954,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3103954"><a href="javascript:void(0);" onclick="return mquote(3103954,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3103954">Can&#039;t wait for this!</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3103954">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.3;msg=3103954">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3103956"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=65182" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=65182" title="View the profile of bisoromi">bisoromi</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3103956_extra_info">
                                <li class="title">Formerly Duwang</li>
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=65182">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=227910;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 196</li><li class="blurb">Location: D[M]V</li>
                                <li class="blurb">owo</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=65182"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=65182" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3103956">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3103956#msg3103956" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #4 on:</strong> Fri, 07 January 2022, 11:37:02 &#187;</div>
                                    <div id="msg_3103956_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3103956;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3103956);">Quote</a></li>
                                    <li class="mquote" id="mquote_3103956"><a href="javascript:void(0);" onclick="return mquote(3103956,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3103956"><a href="javascript:void(0);" onclick="return mquote(3103956,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3103956">will this work with SA</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3103956">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.4;msg=3103956">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3103956_signature"><img src="https://cdn.discordapp.com/attachments/590592322413264900/593125244491923527/dolphbig.png" alt="" width="87" height="33" align="" class="bbc_img resized" /> (credits to <a href="https://geekhack.org/index.php?action=profile;u=75852" class="bbc_link" target="_blank">Kokaloo</a>)</div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3103960"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=123551" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=123551" title="View the profile of Baka Bot">Baka Bot</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3103960_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=123551">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=254719;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 207</li><li class="blurb">Location: idk somewhere in the Western Hemisphere</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=123551"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=123551" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3103960">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3103960#msg3103960" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #5 on:</strong> Fri, 07 January 2022, 11:47:16 &#187;</div>
                                    <div id="msg_3103960_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3103960;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3103960);">Quote</a></li>
                                    <li class="mquote" id="mquote_3103960"><a href="javascript:void(0);" onclick="return mquote(3103960,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3103960"><a href="javascript:void(0);" onclick="return mquote(3103960,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3103960">I am not a fan of the engraving placement. But everything looks fine</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3103960">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.5;msg=3103960">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3103960_signature"><a href="https://geekhack.org/index.php?topic=109545.0" class="bbc_link" target="_blank"><img src="https://cdn.discordapp.com/attachments/776203370015883284/776203614758633482/banner.png" alt="" width="396" height="120" align="" class="bbc_img resized" /></a> <a href="https://geekhack.org/index.php?topic=110650.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/U4UMi8K.png" alt="" width="480" height="120" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3103962"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Online"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useron.gif" alt="Online" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=121512" title="View the profile of kevinave">kevinave</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3103962_extra_info">
                                <li class="stars"></li>
                                <li class="threadstarter">
                                    <b>Thread Starter</b>
                                </li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=121512">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280838;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 19</li><li class="blurb">Location: California</li>
                                <li class="blurb">keebing it cool</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=121512"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3103962" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Personal Message (Online)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_on.gif" alt="Personal Message (Online)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" id="msg_icon_3103962" />
                                    </div>
                                    <h5 id="subject_3103962">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3103962#msg3103962" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #6 on:</strong> Fri, 07 January 2022, 11:49:51 &#187;</div>
                                    <div id="msg_3103962_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3103962;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3103962);">Quote</a></li>
                                    <li class="mquote" id="mquote_3103962"><a href="javascript:void(0);" onclick="return mquote(3103962,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3103962"><a href="javascript:void(0);" onclick="return mquote(3103962,'remove');">Multi-Quote</a></li>
                                    <li class="modify_button"><a href="https://geekhack.org/index.php?action=post;msg=3103962;topic=115887.0">Modify</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3103962"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3103956#msg3103956">Quote from: bisoromi on Fri, 07 January 2022, 11:37:02</a></div></div><blockquote class="bbc_standard_quote">will this work with SA<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div>Assuming that a 1u SA keycap is around 18.20 mm, there should be enough room where there is no interference between the keycaps. That is a good point however and I will mount SA keycaps on the board to verify this weekend. I did not notice any interference with the KAT keycaps I had mounted previously but I will also test those again.</div>
                            </div>
                            <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/modify_inline.gif" alt="Modify message" title="Modify message" class="modifybutton" id="modify_button_3103962" style="cursor: pointer; display: none;" onclick="oQuickModify.modifyMsg('3103962')" />
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3103962">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.6;msg=3103962">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">136.52.119.125</a>
                            </div>
                            <div class="signature" id="msg_3103962_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104003"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=77945" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=77945" title="View the profile of ilikerustoo">ilikerustoo</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104003_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=77945">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=260774;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 127</li><li class="blurb">Location: NJ, USA</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=77945"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3104003" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=77945" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104003">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104003#msg3104003" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #7 on:</strong> Fri, 07 January 2022, 14:46:02 &#187;</div>
                                    <div id="msg_3104003_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104003;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104003);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104003"><a href="javascript:void(0);" onclick="return mquote(3104003,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104003"><a href="javascript:void(0);" onclick="return mquote(3104003,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104003">Cool. Well written post too</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104003">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.7;msg=3104003">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104019"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=148231" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=148231" title="View the profile of beyonddae">beyonddae</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104019_extra_info">
                                <li class="stars"></li>
                                <li class="postcount">Posts: 1</li><li class="blurb">Location: California</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=148231"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=148231" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104019">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104019#msg3104019" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #8 on:</strong> Fri, 07 January 2022, 16:24:38 &#187;</div>
                                    <div id="msg_3104019_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104019;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104019);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104019"><a href="javascript:void(0);" onclick="return mquote(3104019,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104019"><a href="javascript:void(0);" onclick="return mquote(3104019,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104019">hope we&#039;ll get an update on pricing soon! looking forward to this keyboard</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104019">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.8;msg=3104019">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104080"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=84917" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=84917" title="View the profile of Nonnegaard">Nonnegaard</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104080_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=84917">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=276624;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 231</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=84917"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3104080" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=84917" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104080">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104080#msg3104080" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #9 on:</strong> Fri, 07 January 2022, 21:11:06 &#187;</div>
                                    <div id="msg_3104080_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104080;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104080);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104080"><a href="javascript:void(0);" onclick="return mquote(3104080,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104080"><a href="javascript:void(0);" onclick="return mquote(3104080,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104080"><span style="font-family: comic sans ms;" class="bbc_font"><span style="font-size: 18pt;" class="bbc_size"><span style="color: green;" class="bbc_color">to be honest it kinda looks like a mr suit</span></span></span><br /><span style="font-size: 8pt;" class="bbc_size"><sup>jk i&#039;s pretty</sup></span></div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104080">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.9;msg=3104080">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3104080_signature"><div align="center"><strong><span style="font-family: comic sans ms;" class="bbc_font"><span style="font-size: 8pt;" class="bbc_size"><span style="color: red;" class="bbc_color">Keycult No. 1/TKL, Dolphin 2021, Saturn60, Melody65, Gherkin, Model M, 5°, NCR80, M0110-A</span></span></span></strong></div></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104081"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=84917" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=84917" title="View the profile of Nonnegaard">Nonnegaard</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104081_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=84917">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=276624;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 231</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=84917"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3104081" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=84917" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104081">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104081#msg3104081" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #10 on:</strong> Fri, 07 January 2022, 21:12:17 &#187;</div>
                                    <div id="msg_3104081_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104081;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104081);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104081"><a href="javascript:void(0);" onclick="return mquote(3104081,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104081"><a href="javascript:void(0);" onclick="return mquote(3104081,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104081"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3103960#msg3103960">Quote from: Baka Bot on Fri, 07 January 2022, 11:47:16</a></div></div><blockquote class="bbc_standard_quote">I am not a fan of the engraving placement. But everything looks fine<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div>the tall flower is prolly the main selling point doe&nbsp; <img src="https://cdn.geekhack.org/Smileys/solosmileys/blank.gif" alt="&#58;blank&#58;" title="blank" class="smiley" /></div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104081">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.10;msg=3104081">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3104081_signature"><div align="center"><strong><span style="font-family: comic sans ms;" class="bbc_font"><span style="font-size: 8pt;" class="bbc_size"><span style="color: red;" class="bbc_color">Keycult No. 1/TKL, Dolphin 2021, Saturn60, Melody65, Gherkin, Model M, 5°, NCR80, M0110-A</span></span></span></strong></div></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104272"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=117489" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=117489" title="View the profile of kloster_boy">kloster_boy</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104272_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=117489">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280894;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 1</li><li class="blurb">Location: California</li><li class="im_icons">        <ul><li><a class="aim" href="aim:goim?screenname=K105TY&amp;message=Hi.+Are+you+there?" title="AOL Instant Messenger - K105TY"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/aim.gif" alt="AOL Instant Messenger - K105TY" /></a></li>        </ul>    </li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=117489"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=117489" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104272">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104272#msg3104272" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #11 on:</strong> Sat, 08 January 2022, 22:43:33 &#187;</div>
                                    <div id="msg_3104272_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104272;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104272);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104272"><a href="javascript:void(0);" onclick="return mquote(3104272,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104272"><a href="javascript:void(0);" onclick="return mquote(3104272,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104272">awwwweeeee yea!!! calla time this is such a sick board i love the idea of less space between the caps</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104272">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.11;msg=3104272">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3104272_signature">Jelly Epoch SSE; Bubble75; AV3; Biscutneko, Prime_E; KBD75; Skeletn87</div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104328"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=86942" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=86942" title="View the profile of dietonto">dietonto</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104328_extra_info">
                                <li class="stars"></li>
                                <li class="postcount">Posts: 16</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=86942"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=86942" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104328">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104328#msg3104328" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #12 on:</strong> Sun, 09 January 2022, 10:31:55 &#187;</div>
                                    <div id="msg_3104328_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104328;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104328);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104328"><a href="javascript:void(0);" onclick="return mquote(3104328,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104328"><a href="javascript:void(0);" onclick="return mquote(3104328,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104328">Very well written IC.&nbsp; <img src="https://cdn.geekhack.org/Smileys/solosmileys/thumbsup.gif" alt="&#58;thumb&#58;" title="Thumbs up!" class="smiley" /></div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104328">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.12;msg=3104328">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104332"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=129694" title="Online"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useron.gif" alt="Online" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=129694" title="View the profile of Keeblet_257">Keeblet_257</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104332_extra_info">
                                <li class="stars"></li>
                                <li class="postcount">Posts: 92</li><li class="blurb">Location: inside a house maybe</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=129694"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=129694" title="Personal Message (Online)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_on.gif" alt="Personal Message (Online)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104332">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104332#msg3104332" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #13 on:</strong> Sun, 09 January 2022, 10:44:39 &#187;</div>
                                    <div id="msg_3104332_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104332;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104332);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104332"><a href="javascript:void(0);" onclick="return mquote(3104332,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104332"><a href="javascript:void(0);" onclick="return mquote(3104332,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104332">looks like a 500 units total GB</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104332">
                                &#171; <em>Last Edit: Tue, 11 January 2022, 13:18:38 by Keeblet_257</em> &#187;
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.13;msg=3104332">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104365"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=133448" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=133448" title="View the profile of gotgoodiez">gotgoodiez</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104365_extra_info">
                                <li class="stars"></li>
                                <li class="postcount">Posts: 33</li><li class="blurb">Location: USA</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=133448"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=133448" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104365">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104365#msg3104365" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #14 on:</strong> Sun, 09 January 2022, 12:53:34 &#187;</div>
                                    <div id="msg_3104365_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104365;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104365);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104365"><a href="javascript:void(0);" onclick="return mquote(3104365,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104365"><a href="javascript:void(0);" onclick="return mquote(3104365,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104365">I like this! I will keep an eye on this project.</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104365">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.14;msg=3104365">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3104365_signature"><a href="https://geekhack.org/index.php?topic=114297.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/0UNFCYV.png" alt="" width="480" height="120" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104402"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=28894" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=28894" title="View the profile of Puddsy">Puddsy</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104402_extra_info">
                                <li class="title">nice</li>
                                <li class="membergroup"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/../../../Smileys/aaron/Star16_Elated.png" alt="*" />&nbsp;<span class=membergroup>Elated Elder </span></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=28894">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280721;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 11942</li><li class="blurb">Location: RSTLN E</li>
                                <li class="blurb">&quot;Do you shovel to survive, or survive to shovel?&quot;</li><li class="im_icons">        <ul>        </ul>    </li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=28894"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="http://twitch.tv/puddsy" title="" target="_blank" class="new_win"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/www_sm.gif" alt="" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=28894" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li><li><a href="http://www.heatware.com/eval.php?id=93500">
<img src="https://cdn.geekhack.org/Themes/default/images/heat.png" alt="Heatware Evals" />
</a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104402">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104402#msg3104402" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #15 on:</strong> Sun, 09 January 2022, 15:17:47 &#187;</div>
                                    <div id="msg_3104402_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104402;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104402);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104402"><a href="javascript:void(0);" onclick="return mquote(3104402,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104402"><a href="javascript:void(0);" onclick="return mquote(3104402,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104402">what advantage does the smaller spacing provide beyond making PCBs harder to replace?<br /><br />some of the earlier duck boards have 19mm spacing and they were a nightmare to find replacements for until recently. </div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104402">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.15;msg=3104402">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3104402_signature"><span style="color: black;" class="bbc_color">QFR</span> | <span style="color: gold;" class="bbc_color">MJ2 TKL</span> | <span style="color: brown;" class="bbc_color">&quot;Bulgogiboard&quot; (Keycon 104)</span> | <span style="color: purple;" class="bbc_color">ctrlalt x GON 60%</span> | <span style="color: pink;" class="bbc_color">TGR Alice</span> | <span style="color: lightblue;" class="bbc_color">Mira SE</span> | <span style="color: white;" class="bbc_color">Revo One </span> | <span style="color: black;" class="bbc_color"> z </span> | <span style="color: purple;" class="bbc_color">Keycult No. 1</span> | <span style="color: beige;" class="bbc_color">AIS65</span> | <span style="color: maroon;" class="bbc_color">CW80 Proto</span> | <span style="color: orange;" class="bbc_color">Mech27v1</span> | <span style="color: red;" class="bbc_color">Camp C225</span> | <span style="color: teal;" class="bbc_color"> Orion V1 </span><br /><br /><img src="https://i.imgur.com/KYmlfHG.png" alt="" width="290" height="67" align="" class="bbc_img resized" /><br /><br />&quot;Everything is worse, but in a barely perceptible and indefinable way&quot; -dollartacos, after I came back from a break | &quot;Is Linkshine our Nixon?&quot; -NAV | &quot;Puddsy is the Puddsy of keebs&quot; -ns90</div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104404"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=130527" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=130527" title="View the profile of DaaDaa">DaaDaa</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104404_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=130527">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=275729;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 134</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=130527"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3104404" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=130527" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104404">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104404#msg3104404" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #16 on:</strong> Sun, 09 January 2022, 15:21:34 &#187;</div>
                                    <div id="msg_3104404_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104404;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104404);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104404"><a href="javascript:void(0);" onclick="return mquote(3104404,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104404"><a href="javascript:void(0);" onclick="return mquote(3104404,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104404">is there a list of &quot;safe&quot; keycap sets that are guaranteed to work fine with the reduced spacing? do KAT sets work? or can you say that all GMK will work?</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104404">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.16;msg=3104404">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104406"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=129101" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=129101" title="View the profile of beelzking">beelzking</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104406_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=129101">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280410;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 4</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=129101"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=129101" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104406">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104406#msg3104406" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #17 on:</strong> Sun, 09 January 2022, 15:42:14 &#187;</div>
                                    <div id="msg_3104406_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104406;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104406);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104406"><a href="javascript:void(0);" onclick="return mquote(3104406,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104406"><a href="javascript:void(0);" onclick="return mquote(3104406,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104406"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3103960#msg3103960">Quote from: Baka Bot on Fri, 07 January 2022, 11:47:16</a></div></div><blockquote class="bbc_standard_quote">I am not a fan of the engraving placement. But everything looks fine<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div>this one. will there be an option to opt-out of the engraving part? </div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104406">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.17;msg=3104406">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104407"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Online"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useron.gif" alt="Online" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=121512" title="View the profile of kevinave">kevinave</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104407_extra_info">
                                <li class="stars"></li>
                                <li class="threadstarter">
                                    <b>Thread Starter</b>
                                </li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=121512">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280838;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 19</li><li class="blurb">Location: California</li>
                                <li class="blurb">keebing it cool</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=121512"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3104407" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Personal Message (Online)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_on.gif" alt="Personal Message (Online)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" id="msg_icon_3104407" />
                                    </div>
                                    <h5 id="subject_3104407">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104407#msg3104407" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #18 on:</strong> Sun, 09 January 2022, 15:42:45 &#187;</div>
                                    <div id="msg_3104407_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104407;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104407);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104407"><a href="javascript:void(0);" onclick="return mquote(3104407,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104407"><a href="javascript:void(0);" onclick="return mquote(3104407,'remove');">Multi-Quote</a></li>
                                    <li class="modify_button"><a href="https://geekhack.org/index.php?action=post;msg=3104407;topic=115887.0">Modify</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104407"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104402#msg3104402">Quote from: Puddsy on Sun, 09 January 2022, 15:17:47</a></div></div><blockquote class="bbc_standard_quote">what advantage does the smaller spacing provide beyond making PCBs harder to replace?<br /><br />some of the earlier duck boards have 19mm spacing and they were a nightmare to find replacements for until recently.<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />I opted for a lower switch spacing to reduce the gap between the edges of the keycaps and because I found it interesting and thought it was a neat design challenge. I realize that finding replacement PCBs will be a nightmare without any options from me, so I plan on running annual PCB group buys so no one will be left with a glorified paperweight. If I am no longer able to run these yearly groupbuys, I am not opposed to open-sourcing my PCB so people may order/modify themselves.</div>
                            </div>
                            <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/modify_inline.gif" alt="Modify message" title="Modify message" class="modifybutton" id="modify_button_3104407" style="cursor: pointer; display: none;" onclick="oQuickModify.modifyMsg('3104407')" />
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104407">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.18;msg=3104407">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">136.52.119.125</a>
                            </div>
                            <div class="signature" id="msg_3104407_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104409"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Online"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useron.gif" alt="Online" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=121512" title="View the profile of kevinave">kevinave</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104409_extra_info">
                                <li class="stars"></li>
                                <li class="threadstarter">
                                    <b>Thread Starter</b>
                                </li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=121512">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280838;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 19</li><li class="blurb">Location: California</li>
                                <li class="blurb">keebing it cool</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=121512"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3104409" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Personal Message (Online)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_on.gif" alt="Personal Message (Online)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" id="msg_icon_3104409" />
                                    </div>
                                    <h5 id="subject_3104409">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104409#msg3104409" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #19 on:</strong> Sun, 09 January 2022, 15:45:16 &#187;</div>
                                    <div id="msg_3104409_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104409;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104409);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104409"><a href="javascript:void(0);" onclick="return mquote(3104409,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104409"><a href="javascript:void(0);" onclick="return mquote(3104409,'remove');">Multi-Quote</a></li>
                                    <li class="modify_button"><a href="https://geekhack.org/index.php?action=post;msg=3104409;topic=115887.0">Modify</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104409"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104404#msg3104404">Quote from: DaaDaa on Sun, 09 January 2022, 15:21:34</a></div></div><blockquote class="bbc_standard_quote">is there a list of &quot;safe&quot; keycap sets that are guaranteed to work fine with the reduced spacing? do KAT sets work? or can you say that all GMK will work?<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />I hope to get pictures of and my thoughts on KAT, MT3, and EPBT sets up by today. Sadly I was not able to borrow a SA set this weekend but I will be looking to mount SA and GMK sets in the coming weeks to verify compatibility.</div>
                            </div>
                            <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/modify_inline.gif" alt="Modify message" title="Modify message" class="modifybutton" id="modify_button_3104409" style="cursor: pointer; display: none;" onclick="oQuickModify.modifyMsg('3104409')" />
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104409">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.19;msg=3104409">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">136.52.119.125</a>
                            </div>
                            <div class="signature" id="msg_3104409_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104411"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Online"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useron.gif" alt="Online" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=121512" title="View the profile of kevinave">kevinave</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104411_extra_info">
                                <li class="stars"></li>
                                <li class="threadstarter">
                                    <b>Thread Starter</b>
                                </li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=121512">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280838;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 19</li><li class="blurb">Location: California</li>
                                <li class="blurb">keebing it cool</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=121512"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3104411" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Personal Message (Online)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_on.gif" alt="Personal Message (Online)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" id="msg_icon_3104411" />
                                    </div>
                                    <h5 id="subject_3104411">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104411#msg3104411" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #20 on:</strong> Sun, 09 January 2022, 15:47:37 &#187;</div>
                                    <div id="msg_3104411_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104411;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104411);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104411"><a href="javascript:void(0);" onclick="return mquote(3104411,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104411"><a href="javascript:void(0);" onclick="return mquote(3104411,'remove');">Multi-Quote</a></li>
                                    <li class="modify_button"><a href="https://geekhack.org/index.php?action=post;msg=3104411;topic=115887.0">Modify</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104411"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104406#msg3104406">Quote from: beelzking on Sun, 09 January 2022, 15:42:14</a></div></div><blockquote class="bbc_standard_quote"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3103960#msg3103960">Quote from: Baka Bot on Fri, 07 January 2022, 11:47:16</a></div></div><blockquote class="bbc_alternate_quote">I am not a fan of the engraving placement. But everything looks fine<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div>this one. will there be an option to opt-out of the engraving part?<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />With the current unit count, I doubt I would be able to provide an option to opt out of the top engraving. That said, if there is enough interest that I could increase unit count, I am not opposed to adding this as an option if there are no downsides.</div>
                            </div>
                            <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/modify_inline.gif" alt="Modify message" title="Modify message" class="modifybutton" id="modify_button_3104411" style="cursor: pointer; display: none;" onclick="oQuickModify.modifyMsg('3104411')" />
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104411">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.20;msg=3104411">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">136.52.119.125</a>
                            </div>
                            <div class="signature" id="msg_3104411_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104418"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=28894" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=28894" title="View the profile of Puddsy">Puddsy</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104418_extra_info">
                                <li class="title">nice</li>
                                <li class="membergroup"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/../../../Smileys/aaron/Star16_Elated.png" alt="*" />&nbsp;<span class=membergroup>Elated Elder </span></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=28894">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280721;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 11942</li><li class="blurb">Location: RSTLN E</li>
                                <li class="blurb">&quot;Do you shovel to survive, or survive to shovel?&quot;</li><li class="im_icons">        <ul>        </ul>    </li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=28894"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="http://twitch.tv/puddsy" title="" target="_blank" class="new_win"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/www_sm.gif" alt="" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=28894" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li><li><a href="http://www.heatware.com/eval.php?id=93500">
<img src="https://cdn.geekhack.org/Themes/default/images/heat.png" alt="Heatware Evals" />
</a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104418">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104418#msg3104418" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #21 on:</strong> Sun, 09 January 2022, 16:14:30 &#187;</div>
                                    <div id="msg_3104418_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104418;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104418);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104418"><a href="javascript:void(0);" onclick="return mquote(3104418,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104418"><a href="javascript:void(0);" onclick="return mquote(3104418,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104418"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104407#msg3104407">Quote from: kevinave on Sun, 09 January 2022, 15:42:45</a></div></div><blockquote class="bbc_standard_quote"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104402#msg3104402">Quote from: Puddsy on Sun, 09 January 2022, 15:17:47</a></div></div><blockquote class="bbc_alternate_quote">what advantage does the smaller spacing provide beyond making PCBs harder to replace?<br /><br />some of the earlier duck boards have 19mm spacing and they were a nightmare to find replacements for until recently.<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />I opted for a lower switch spacing to reduce the gap between the edges of the keycaps and because I found it interesting and thought it was a neat design challenge. I realize that finding replacement PCBs will be a nightmare without any options from me, so I plan on running annual PCB group buys so no one will be left with a glorified paperweight. If I am no longer able to run these yearly groupbuys, I am not opposed to open-sourcing my PCB so people may order/modify themselves.<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />neat design challenge is good enough for me. it&#039;s a little unclear from the original post WHY exactly you went for it but i can accept &quot;i thought it would be cool&quot; over trying to make up some random unnecessary reason for it. <br /><br />advising people to order an extra PCB plate is pretty wise as well, just in case. part of the reason people started offering that in the first place is because it was much harder to get extra parts after the GB until around 2018-2019. </div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104418">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.21;msg=3104418">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3104418_signature"><span style="color: black;" class="bbc_color">QFR</span> | <span style="color: gold;" class="bbc_color">MJ2 TKL</span> | <span style="color: brown;" class="bbc_color">&quot;Bulgogiboard&quot; (Keycon 104)</span> | <span style="color: purple;" class="bbc_color">ctrlalt x GON 60%</span> | <span style="color: pink;" class="bbc_color">TGR Alice</span> | <span style="color: lightblue;" class="bbc_color">Mira SE</span> | <span style="color: white;" class="bbc_color">Revo One </span> | <span style="color: black;" class="bbc_color"> z </span> | <span style="color: purple;" class="bbc_color">Keycult No. 1</span> | <span style="color: beige;" class="bbc_color">AIS65</span> | <span style="color: maroon;" class="bbc_color">CW80 Proto</span> | <span style="color: orange;" class="bbc_color">Mech27v1</span> | <span style="color: red;" class="bbc_color">Camp C225</span> | <span style="color: teal;" class="bbc_color"> Orion V1 </span><br /><br /><img src="https://i.imgur.com/KYmlfHG.png" alt="" width="290" height="67" align="" class="bbc_img resized" /><br /><br />&quot;Everything is worse, but in a barely perceptible and indefinable way&quot; -dollartacos, after I came back from a break | &quot;Is Linkshine our Nixon?&quot; -NAV | &quot;Puddsy is the Puddsy of keebs&quot; -ns90</div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104431"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=140431" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=140431" title="View the profile of Mecxs">Mecxs</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104431_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=140431">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=275687;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 128</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=140431"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=140431" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104431">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104431#msg3104431" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #22 on:</strong> Sun, 09 January 2022, 17:24:58 &#187;</div>
                                    <div id="msg_3104431_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104431;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104431);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104431"><a href="javascript:void(0);" onclick="return mquote(3104431,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104431"><a href="javascript:void(0);" onclick="return mquote(3104431,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104431"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104332#msg3104332">Quote from: Keeblet_257 on Sun, 09 January 2022, 10:44:39</a></div></div><blockquote class="bbc_standard_quote">looks like a 500 units total GB and if this number gets splitup and region locked it basically means that EU will only get a maximum of 50-100 untis.<br />So getting this board is basically impossible D:<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />500? This is 35 units according to OP.</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104431">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.22;msg=3104431">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104437"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=61264" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=61264" title="View the profile of moonmaster">moonmaster</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104437_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=61264">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=166328;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 87</li><li class="blurb">Location: Los Angeles, CA</li>
                                <li class="blurb">big bumps, beautiful boards</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=61264"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=61264" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104437">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104437#msg3104437" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #23 on:</strong> Sun, 09 January 2022, 17:54:26 &#187;</div>
                                    <div id="msg_3104437_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104437;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104437);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104437"><a href="javascript:void(0);" onclick="return mquote(3104437,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104437"><a href="javascript:void(0);" onclick="return mquote(3104437,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104437">Color me interested. Any chance of doing an open quantity GB? Or something like 500 units or 750 unit max? <br /><br />Sent from my LE2125 using Tapatalk<br /><br /></div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104437">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.23;msg=3104437">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104443"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=134273" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=134273" title="View the profile of Nurseh">Nurseh</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104443_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=134273">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=282475;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 61</li><li class="blurb">Location: Maple Syrup Land</li>
                                <li class="blurb">Sorry for always apologizing...</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=134273"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=134273" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104443">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104443#msg3104443" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #24 on:</strong> Sun, 09 January 2022, 18:25:07 &#187;</div>
                                    <div id="msg_3104443_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104443;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104443);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104443"><a href="javascript:void(0);" onclick="return mquote(3104443,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104443"><a href="javascript:void(0);" onclick="return mquote(3104443,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104443">Love things are are different from the norm, has there been any issues of clearance on anything that is being looked at?</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104443">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.24;msg=3104443">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3104443_signature"><a href="https://geekhack.org/index.php?topic=108227" class="bbc_link" target="_blank"><img src="https://i.imgur.com/j92Ngqo.png" alt="" width="300" height="120" align="" class="bbc_img resized" /></a><a href="https://geekhack.org/index.php?topic=110967.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/AYtifVh.gif" alt="" width="300" height="120" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104452"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=130527" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=130527" title="View the profile of DaaDaa">DaaDaa</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104452_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=130527">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=275729;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 134</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=130527"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3104452" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=130527" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104452">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104452#msg3104452" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #25 on:</strong> Sun, 09 January 2022, 18:52:26 &#187;</div>
                                    <div id="msg_3104452_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104452;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104452);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104452"><a href="javascript:void(0);" onclick="return mquote(3104452,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104452"><a href="javascript:void(0);" onclick="return mquote(3104452,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104452"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104332#msg3104332">Quote from: Keeblet_257 on Sun, 09 January 2022, 10:44:39</a></div></div><blockquote class="bbc_standard_quote">looks like a 500 units total GB and if this number gets splitup and region locked it basically means that EU will only get a maximum of 50-100 untis.<br />So getting this board is basically impossible D:<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />LOL ... what are you on?</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104452">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.25;msg=3104452">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104453"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Online"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useron.gif" alt="Online" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=121512" title="View the profile of kevinave">kevinave</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104453_extra_info">
                                <li class="stars"></li>
                                <li class="threadstarter">
                                    <b>Thread Starter</b>
                                </li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=121512">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280838;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 19</li><li class="blurb">Location: California</li>
                                <li class="blurb">keebing it cool</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=121512"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3104453" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Personal Message (Online)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_on.gif" alt="Personal Message (Online)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" id="msg_icon_3104453" />
                                    </div>
                                    <h5 id="subject_3104453">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104453#msg3104453" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #26 on:</strong> Sun, 09 January 2022, 18:56:42 &#187;</div>
                                    <div id="msg_3104453_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104453;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104453);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104453"><a href="javascript:void(0);" onclick="return mquote(3104453,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104453"><a href="javascript:void(0);" onclick="return mquote(3104453,'remove');">Multi-Quote</a></li>
                                    <li class="modify_button"><a href="https://geekhack.org/index.php?action=post;msg=3104453;topic=115887.0">Modify</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104453">I added a section underneath my prototype post dedicated to mounting different keycaps to verify compatibility to address concerns and will try to cover as many profiles and manufacturers as possible in order to make sure there are no issues.</div>
                            </div>
                            <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/modify_inline.gif" alt="Modify message" title="Modify message" class="modifybutton" id="modify_button_3104453" style="cursor: pointer; display: none;" onclick="oQuickModify.modifyMsg('3104453')" />
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104453">
                                &#171; <em>Last Edit: Mon, 10 January 2022, 03:58:07 by kevinave</em> &#187;
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.26;msg=3104453">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">136.52.119.125</a>
                            </div>
                            <div class="signature" id="msg_3104453_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104456"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Online"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useron.gif" alt="Online" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=121512" title="View the profile of kevinave">kevinave</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104456_extra_info">
                                <li class="stars"></li>
                                <li class="threadstarter">
                                    <b>Thread Starter</b>
                                </li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=121512">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280838;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 19</li><li class="blurb">Location: California</li>
                                <li class="blurb">keebing it cool</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=121512"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3104456" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Personal Message (Online)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_on.gif" alt="Personal Message (Online)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" id="msg_icon_3104456" />
                                    </div>
                                    <h5 id="subject_3104456">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104456#msg3104456" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #27 on:</strong> Sun, 09 January 2022, 19:18:31 &#187;</div>
                                    <div id="msg_3104456_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104456;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104456);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104456"><a href="javascript:void(0);" onclick="return mquote(3104456,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104456"><a href="javascript:void(0);" onclick="return mquote(3104456,'remove');">Multi-Quote</a></li>
                                    <li class="modify_button"><a href="https://geekhack.org/index.php?action=post;msg=3104456;topic=115887.0">Modify</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104456"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104332#msg3104332">Quote from: Keeblet_257 on Sun, 09 January 2022, 10:44:39</a></div></div><blockquote class="bbc_standard_quote">looks like a 500 units total GB and if this number gets splitup and region locked it basically means that EU will only get a maximum of 50-100 untis.<br />So getting this board is basically impossible D:<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br /><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104437#msg3104437">Quote from: moonmaster on Sun, 09 January 2022, 17:54:26</a></div></div><blockquote class="bbc_standard_quote">Color me interested. Any chance of doing an open quantity GB? Or something like 500 units or 750 unit max? <br /><br />Sent from my LE2125 using Tapatalk<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />I mentioned this in the IC but I chose a 35 unit count as this is the first group buy I am running and I don&#039;t want to bite off more than I can chew (I can already see 35 units being a daunting task to fulfill from a QC and shipping perspective). That said, I am closely monitoring the IC form and overall interest for the board. On the small chance that there is a need to increase unit count, albeit probably not to such high numbers like 500-750, I will reach out to vendors.</div>
                            </div>
                            <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/modify_inline.gif" alt="Modify message" title="Modify message" class="modifybutton" id="modify_button_3104456" style="cursor: pointer; display: none;" onclick="oQuickModify.modifyMsg('3104456')" />
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104456">
                                &#171; <em>Last Edit: Sun, 09 January 2022, 20:36:24 by kevinave</em> &#187;
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.27;msg=3104456">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">136.52.119.125</a>
                            </div>
                            <div class="signature" id="msg_3104456_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104704"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=144925" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=144925" title="View the profile of whitewolf154">whitewolf154</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104704_extra_info">
                                <li class="stars"></li>
                                <li class="postcount">Posts: 9</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=144925"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=144925" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104704">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104704#msg3104704" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #28 on:</strong> Mon, 10 January 2022, 19:02:47 &#187;</div>
                                    <div id="msg_3104704_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104704;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104704);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104704"><a href="javascript:void(0);" onclick="return mquote(3104704,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104704"><a href="javascript:void(0);" onclick="return mquote(3104704,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104704">I feel like OP is very dedicated, and I really hope he can keep up the energy. Although this is his first run, I feel somewhat relieved</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104704">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.28;msg=3104704">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104718"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=111497" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=111497" title="View the profile of alwaysbless">alwaysbless</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104718_extra_info">
                                <li class="stars"></li>
                                <li class="postcount">Posts: 108</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=111497"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=111497" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104718">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104718#msg3104718" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #29 on:</strong> Mon, 10 January 2022, 20:03:43 &#187;</div>
                                    <div id="msg_3104718_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104718;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104718);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104718"><a href="javascript:void(0);" onclick="return mquote(3104718,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104718"><a href="javascript:void(0);" onclick="return mquote(3104718,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104718">Bottom looks like Elite and Bias combined. </div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104718">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.29;msg=3104718">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104739"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Online"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useron.gif" alt="Online" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=121512" title="View the profile of kevinave">kevinave</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104739_extra_info">
                                <li class="stars"></li>
                                <li class="threadstarter">
                                    <b>Thread Starter</b>
                                </li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=121512">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280838;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 19</li><li class="blurb">Location: California</li>
                                <li class="blurb">keebing it cool</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=121512"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3104739" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Personal Message (Online)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_on.gif" alt="Personal Message (Online)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" id="msg_icon_3104739" />
                                    </div>
                                    <h5 id="subject_3104739">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104739#msg3104739" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #30 on:</strong> Mon, 10 January 2022, 22:54:13 &#187;</div>
                                    <div id="msg_3104739_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104739;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104739);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104739"><a href="javascript:void(0);" onclick="return mquote(3104739,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104739"><a href="javascript:void(0);" onclick="return mquote(3104739,'remove');">Multi-Quote</a></li>
                                    <li class="modify_button"><a href="https://geekhack.org/index.php?action=post;msg=3104739;topic=115887.0">Modify</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104739"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104704#msg3104704">Quote from: whitewolf154 on Mon, 10 January 2022, 19:02:47</a></div></div><blockquote class="bbc_standard_quote">I feel like OP is very dedicated, and I really hope he can keep up the energy. Although this is his first run, I feel somewhat relieved<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div>Thank you and I am very glad that I was able to relieve a bit of the apprehension that comes from a project led by a first-time runner such as myself. <br /><br /><br /><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104718#msg3104718">Quote from: alwaysbless on Mon, 10 January 2022, 20:03:43</a></div></div><blockquote class="bbc_standard_quote">Bottom looks like Elite and Bias combined.<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div>The bottoms of both of those boards are absolutely stunning and I find the comparison flattering.&nbsp; </div>
                            </div>
                            <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/modify_inline.gif" alt="Modify message" title="Modify message" class="modifybutton" id="modify_button_3104739" style="cursor: pointer; display: none;" onclick="oQuickModify.modifyMsg('3104739')" />
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104739">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.30;msg=3104739">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">136.52.119.125</a>
                            </div>
                            <div class="signature" id="msg_3104739_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104742"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=126447" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=126447" title="View the profile of shima">shima</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104742_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=126447">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=279071;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 63</li><li class="blurb">Location: California</li>
                                <li class="blurb">keeb weeb</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=126447"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=126447" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104742">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104742#msg3104742" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #31 on:</strong> Mon, 10 January 2022, 23:05:01 &#187;</div>
                                    <div id="msg_3104742_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104742;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104742);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104742"><a href="javascript:void(0);" onclick="return mquote(3104742,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104742"><a href="javascript:void(0);" onclick="return mquote(3104742,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104742"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104718#msg3104718">Quote from: alwaysbless on Mon, 10 January 2022, 20:03:43</a></div></div><blockquote class="bbc_standard_quote">Bottom looks like Elite and Bias combined.<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div>I mean, you can say that Bias takes inspiration from the C225 if you&#039;re going off of that. Hard to really do much imo but eh. Although ngl, don&#039;t really see the Elite similarities like at all</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104742">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.31;msg=3104742">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3104742_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a><a href="https://geekhack.org/index.php?topic=116187.0" class="bbc_link" target="_blank"><img src="https://imgur.com/uqxW4c9.png" alt="" width="288" height="120" align="" class="bbc_img resized" /></a><br /><br />Palette G67 | Kyuu | Biscutneko | F1-8X</div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104815"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=111497" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=111497" title="View the profile of alwaysbless">alwaysbless</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104815_extra_info">
                                <li class="stars"></li>
                                <li class="postcount">Posts: 108</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=111497"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=111497" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104815">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104815#msg3104815" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #32 on:</strong> Tue, 11 January 2022, 11:36:53 &#187;</div>
                                    <div id="msg_3104815_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104815;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104815);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104815"><a href="javascript:void(0);" onclick="return mquote(3104815,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104815"><a href="javascript:void(0);" onclick="return mquote(3104815,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104815"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104742#msg3104742">Quote from: shima on Mon, 10 January 2022, 23:05:01</a></div></div><blockquote class="bbc_standard_quote"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104718#msg3104718">Quote from: alwaysbless on Mon, 10 January 2022, 20:03:43</a></div></div><blockquote class="bbc_alternate_quote">Bottom looks like Elite and Bias combined.<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div>I mean, you can say that Bias takes inspiration from the C225 if you&#039;re going off of that. Hard to really do much imo but eh. Although ngl, don&#039;t really see the Elite similarities like at all<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />C225 bottom looks more like a keycult to me. But as far as the elite its the side ripple that looks similar imo. Either way nice combination of the two which is something that has not been done before. <br /><br /><a href="https://i.imgur.com/2M0NgLw.jpg" class="bbc_link" target="_blank">https://i.imgur.com/2M0NgLw.jpg</a></div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104815">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.32;msg=3104815">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3104918"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=134538" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=134538" title="View the profile of POMChamp">POMChamp</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3104918_extra_info">
                                <li class="stars"></li>
                                <li class="postcount">Posts: 2</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=134538"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=134538" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3104918">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3104918#msg3104918" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #33 on:</strong> Tue, 11 January 2022, 19:30:48 &#187;</div>
                                    <div id="msg_3104918_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3104918;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3104918);">Quote</a></li>
                                    <li class="mquote" id="mquote_3104918"><a href="javascript:void(0);" onclick="return mquote(3104918,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3104918"><a href="javascript:void(0);" onclick="return mquote(3104918,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3104918">I&#039;m impressed with how well-written your IC is and wish you the best with your first GB!</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3104918">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.33;msg=3104918">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3105021"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=129101" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=129101" title="View the profile of beelzking">beelzking</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3105021_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=129101">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280410;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 4</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=129101"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=129101" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3105021">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3105021#msg3105021" rel="nofollow">Re: [IC] Calla - Seamless F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #34 on:</strong> Wed, 12 January 2022, 10:06:19 &#187;</div>
                                    <div id="msg_3105021_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3105021;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3105021);">Quote</a></li>
                                    <li class="mquote" id="mquote_3105021"><a href="javascript:void(0);" onclick="return mquote(3105021,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3105021"><a href="javascript:void(0);" onclick="return mquote(3105021,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3105021"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104411#msg3104411">Quote from: kevinave on Sun, 09 January 2022, 15:47:37</a></div></div><blockquote class="bbc_standard_quote"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3104406#msg3104406">Quote from: beelzking on Sun, 09 January 2022, 15:42:14</a></div></div><blockquote class="bbc_alternate_quote"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3103960#msg3103960">Quote from: Baka Bot on Fri, 07 January 2022, 11:47:16</a></div></div><blockquote class="bbc_standard_quote">I am not a fan of the engraving placement. But everything looks fine<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div>this one. will there be an option to opt-out of the engraving part?<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />With the current unit count, I doubt I would be able to provide an option to opt out of the top engraving. That said, if there is enough interest that I could increase unit count, I am not opposed to adding this as an option if there are no downsides.<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />ic, no problem. This is a pretty good looking board and a pretty good IC for your first ever run, GLWIC.</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3105021">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.34;msg=3105021">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3105037"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=147007" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=147007" title="View the profile of hussar_name">hussar_name</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3105037_extra_info">
                                <li class="stars"></li>
                                <li class="postcount">Posts: 63</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=147007"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=147007" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3105037">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3105037#msg3105037" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #35 on:</strong> Wed, 12 January 2022, 12:03:53 &#187;</div>
                                    <div id="msg_3105037_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3105037;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3105037);">Quote</a></li>
                                    <li class="mquote" id="mquote_3105037"><a href="javascript:void(0);" onclick="return mquote(3105037,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3105037"><a href="javascript:void(0);" onclick="return mquote(3105037,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3105037">&nbsp;<img src="https://cdn.geekhack.org/Smileys/solosmileys/smiley.gif" alt="&#58;&#41;" title="Smiley" class="smiley" />)<br /><br />What can possibly go wrong.<br /><br /><img src="https://cdn.geekhack.org/Smileys/solosmileys/smiley.gif" alt="&#58;&#41;" title="Smiley" class="smiley" />)</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3105037">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.35;msg=3105037">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3106350"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=134628" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=134628" title="View the profile of atl22033">atl22033</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3106350_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=134628">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=269270;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 52</li>
                                <li class="blurb">Signature art by Shima</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=134628"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=134628" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3106350">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3106350#msg3106350" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #36 on:</strong> Wed, 19 January 2022, 18:32:26 &#187;</div>
                                    <div id="msg_3106350_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3106350;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3106350);">Quote</a></li>
                                    <li class="mquote" id="mquote_3106350"><a href="javascript:void(0);" onclick="return mquote(3106350,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3106350"><a href="javascript:void(0);" onclick="return mquote(3106350,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3106350">gib me calla</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3106350">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.36;msg=3106350">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3106350_signature"><a href="https://geekhack.org/index.php?topic=114081.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/yyRvLSV.jpg" alt="" width="480" height="120" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3106360"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Online"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useron.gif" alt="Online" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=121512" title="View the profile of kevinave">kevinave</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3106360_extra_info">
                                <li class="stars"></li>
                                <li class="threadstarter">
                                    <b>Thread Starter</b>
                                </li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=121512">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280838;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 19</li><li class="blurb">Location: California</li>
                                <li class="blurb">keebing it cool</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=121512"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3106360" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Personal Message (Online)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_on.gif" alt="Personal Message (Online)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" id="msg_icon_3106360" />
                                    </div>
                                    <h5 id="subject_3106360">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3106360#msg3106360" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #37 on:</strong> Wed, 19 January 2022, 19:49:13 &#187;</div>
                                    <div id="msg_3106360_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3106360;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3106360);">Quote</a></li>
                                    <li class="mquote" id="mquote_3106360"><a href="javascript:void(0);" onclick="return mquote(3106360,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3106360"><a href="javascript:void(0);" onclick="return mquote(3106360,'remove');">Multi-Quote</a></li>
                                    <li class="modify_button"><a href="https://geekhack.org/index.php?action=post;msg=3106360;topic=115887.0">Modify</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3106360"><strong>The second prototype should be ordered shortly after LNY.</strong> Under the main post, there is a list of the details changing between the V1 and V2 prototypes (most of which were made to improve QoL). In the meantime, I recorded a short video featuring the V1 Prototype. Thank you for your continued interest and I will try to make a more in-depth video upon receiving the second prototype.<br /><br /><div class="oharaEmbed youtube" id="oh_VnOIbJmiz0A" style="width: 480px; height: 270px;"></div></div>
                            </div>
                            <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/modify_inline.gif" alt="Modify message" title="Modify message" class="modifybutton" id="modify_button_3106360" style="cursor: pointer; display: none;" onclick="oQuickModify.modifyMsg('3106360')" />
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3106360">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.37;msg=3106360">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">136.52.119.125</a>
                            </div>
                            <div class="signature" id="msg_3106360_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3108238"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=116243" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=116243" title="View the profile of spedywin">spedywin</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3108238_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=116243">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=281232;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 19</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=116243"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=116243" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3108238">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3108238#msg3108238" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #38 on:</strong> Sat, 29 January 2022, 05:26:34 &#187;</div>
                                    <div id="msg_3108238_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3108238;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3108238);">Quote</a></li>
                                    <li class="mquote" id="mquote_3108238"><a href="javascript:void(0);" onclick="return mquote(3108238,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3108238"><a href="javascript:void(0);" onclick="return mquote(3108238,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3108238">lilies r nice</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3108238">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.38;msg=3108238">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3111223"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=126767" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=126767" title="View the profile of genevatypes">genevatypes</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3111223_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=126767">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=281490;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 42</li><li class="blurb">Location: Orange County, CA</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=126767"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=126767" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3111223">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3111223#msg3111223" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #39 on:</strong> Tue, 15 February 2022, 03:30:11 &#187;</div>
                                    <div id="msg_3111223_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3111223;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3111223);">Quote</a></li>
                                    <li class="mquote" id="mquote_3111223"><a href="javascript:void(0);" onclick="return mquote(3111223,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3111223"><a href="javascript:void(0);" onclick="return mquote(3111223,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3111223">calla so hot</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3111223">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.39;msg=3111223">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3112901"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4 style="font-size: 115%">
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=144820" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=144820" title="View the profile of Jewpac Shakur">Jewpac Shakur</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3112901_extra_info">
                                <li class="stars"></li>
                                <li class="postcount">Posts: 8</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=144820"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=144820" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3112901">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3112901#msg3112901" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #40 on:</strong> Fri, 25 February 2022, 13:41:57 &#187;</div>
                                    <div id="msg_3112901_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3112901;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3112901);">Quote</a></li>
                                    <li class="mquote" id="mquote_3112901"><a href="javascript:void(0);" onclick="return mquote(3112901,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3112901"><a href="javascript:void(0);" onclick="return mquote(3112901,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3112901">count me in</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3112901">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.40;msg=3112901">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3112947"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=112389" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=112389" title="View the profile of Jefff">Jefff</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3112947_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=112389">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=258253;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 133</li><li class="blurb">Location: California, USA</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=112389"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://jlabs.co/" title="jlabs.co" target="_blank" class="new_win"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/www_sm.gif" alt="jlabs.co" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3112947" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=112389" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3112947">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3112947#msg3112947" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #41 on:</strong> Fri, 25 February 2022, 20:16:55 &#187;</div>
                                    <div id="msg_3112947_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3112947;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3112947);">Quote</a></li>
                                    <li class="mquote" id="mquote_3112947"><a href="javascript:void(0);" onclick="return mquote(3112947,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3112947"><a href="javascript:void(0);" onclick="return mquote(3112947,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3112947">I imagine keycap pullers are gonna be pretty hard to use with this board... How do you suggest we remove keycaps without exerting too much lateral force on the stems?</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3112947">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.41;msg=3112947">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3112947_signature"><a href="https://geekhack.org/index.php?topic=114043.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/R8tAFb6.png" alt="" width="302" height="120" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3112956"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Online"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useron.gif" alt="Online" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=121512" title="View the profile of kevinave">kevinave</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3112956_extra_info">
                                <li class="stars"></li>
                                <li class="threadstarter">
                                    <b>Thread Starter</b>
                                </li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=121512">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=280838;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 19</li><li class="blurb">Location: California</li>
                                <li class="blurb">keebing it cool</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=121512"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=emailuser;sa=email;msg=3112956" rel="nofollow"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/email_sm.gif" alt="Email" title="Email" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=121512" title="Personal Message (Online)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_on.gif" alt="Personal Message (Online)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" id="msg_icon_3112956" />
                                    </div>
                                    <h5 id="subject_3112956">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3112956#msg3112956" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #42 on:</strong> Fri, 25 February 2022, 21:16:15 &#187;</div>
                                    <div id="msg_3112956_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3112956;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3112956);">Quote</a></li>
                                    <li class="mquote" id="mquote_3112956"><a href="javascript:void(0);" onclick="return mquote(3112956,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3112956"><a href="javascript:void(0);" onclick="return mquote(3112956,'remove');">Multi-Quote</a></li>
                                    <li class="modify_button"><a href="https://geekhack.org/index.php?action=post;msg=3112956;topic=115887.0">Modify</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3112956"><div class="quoteheader"><div class="topslice_quote"><a href="https://geekhack.org/index.php?topic=115887.msg3112947#msg3112947">Quote from: Jefff on Fri, 25 February 2022, 20:16:55</a></div></div><blockquote class="bbc_standard_quote">I imagine keycap pullers are gonna be pretty hard to use with this board... How do you suggest we remove keycaps without exerting too much lateral force on the stems?<br /></blockquote><div class="quotefooter"><div class="botslice_quote"></div></div><br />By lateral force on the stems, is that whether or not the keycap puller would have to displace adjacent keycaps to fit under a keycap? If so, from my testing, a basic keycap puller was still able to fit between most keycaps spaced 18.9 mm apart without having to &quot;push&quot; the keycaps/switch stem of adjacent keys away. <br /><br />It is a valid concern though and reducing the switch spacing does mean that certain keycaps will be harder to remove, something that I have been documenting in detail directly under the IC and in a shortened table that summarizes my findings: <a href="https://docs.google.com/spreadsheets/d/1dD4QSbrBYBxJfmBSrPmv0h0tP35393vytqnkWBa45fE/edit#gid=1241946632" class="bbc_link" target="_blank">https://docs.google.com/spreadsheets/d/1dD4QSbrBYBxJfmBSrPmv0h0tP35393vytqnkWBa45fE/edit#gid=1241946632</a><br /><br />Long story short, I was able to remove all keycaps I tested from the board without having to disassemble the case but for keycaps like MT3 which are vastly larger at the base, I would recommend disassembling the case for ease of mind and access.<br /></div>
                            </div>
                            <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/modify_inline.gif" alt="Modify message" title="Modify message" class="modifybutton" id="modify_button_3112956" style="cursor: pointer; display: none;" onclick="oQuickModify.modifyMsg('3112956')" />
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3112956">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.42;msg=3112956">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">136.52.119.125</a>
                            </div>
                            <div class="signature" id="msg_3112956_signature"><a href="https://geekhack.org/index.php?topic=115887.0" class="bbc_link" target="_blank"><img src="https://i.imgur.com/ef1zFSK.png?2" alt="" width="360" height="100" align="" class="bbc_img resized" /></a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3113085"></a>
                <div class="windowbg2">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=140545" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=140545" title="View the profile of .jan">.jan</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3113085_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=140545">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=283072;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 8</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=140545"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=140545" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3113085">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3113085#msg3113085" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #43 on:</strong> Sun, 27 February 2022, 00:02:26 &#187;</div>
                                    <div id="msg_3113085_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3113085;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3113085);">Quote</a></li>
                                    <li class="mquote" id="mquote_3113085"><a href="javascript:void(0);" onclick="return mquote(3113085,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3113085"><a href="javascript:void(0);" onclick="return mquote(3113085,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3113085">so down for this</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3113085">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.43;msg=3113085">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                <a id="msg3113180"></a>
                <div class="windowbg">
                    <span class="topslice"><span></span></span>
                    <div class="post_wrapper">
                        <div class="poster">
                            <h4>
                                <a href="https://geekhack.org/index.php?action=pm;sa=send;u=132600" title="Offline"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/useroff.gif" alt="Offline" /></a>
                                <a href="https://geekhack.org/index.php?action=profile;u=132600" title="View the profile of Que7797">Que7797</a>
                            </h4>
                            <ul class="reset smalltext" id="msg_3113180_extra_info">
                                <li class="stars"></li>
                                <li class="avatar">
                                    <a href="https://geekhack.org/index.php?action=profile;u=132600">
                                        <img class="avatar" src="https://geekhack.org/index.php?action=dlattach;attach=282979;type=avatar" alt="" />
                                    </a>
                                </li>
                                <li class="postcount">Posts: 56</li>
                                <li class="profile">
                                    <ul>
                                        <li><a href="https://geekhack.org/index.php?action=profile;u=132600"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/icons/profile_sm.gif" alt="View Profile" title="View Profile" /></a></li>
                                        <li><a href="https://geekhack.org/index.php?action=pm;sa=send;u=132600" title="Personal Message (Offline)"><img src="https://cdn.geekhack.org/Themes/Nostalgia/images/im_off.gif" alt="Personal Message (Offline)" /></a></li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        <div class="postarea">
                            <div class="flow_hidden">
                                <div class="keyinfo">
                                    <div class="messageicon">
                                        <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/post/xx.gif" alt="" />
                                    </div>
                                    <h5 id="subject_3113180">
                                        <a href="https://geekhack.org/index.php?topic=115887.msg3113180#msg3113180" rel="nofollow">Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</a>
                                    </h5>
                                    <div class="smalltext">&#171; <strong>Reply #44 on:</strong> Sun, 27 February 2022, 14:19:51 &#187;</div>
                                    <div id="msg_3113180_quick_mod"></div>
                                </div>
                                <ul class="reset smalltext quickbuttons">
                                    <li class="quote_button"><a href="https://geekhack.org/index.php?action=post;quote=3113180;topic=115887.0;last_msg=3113180" onclick="return oQuickReply.quote(3113180);">Quote</a></li>
                                    <li class="mquote" id="mquote_3113180"><a href="javascript:void(0);" onclick="return mquote(3113180,'none');">Multi-Quote</a></li>
                                    <li class="mquote_remove" id="mquote_remove_3113180"><a href="javascript:void(0);" onclick="return mquote(3113180,'remove');">Multi-Quote</a></li>
                                </ul>
                            </div>
                            <div class="post">
                                <div class="inner" id="msg_3113180">The reduced switch spacing is interesting, and what a drastic way to ensure a WKL case! <img src="https://cdn.geekhack.org/Smileys/solosmileys/thumbsup.gif" alt="&#58;thumb&#58;" title="Thumbs up!" class="smiley" /><br /><br />Jokes aside, this looks great. I&#039;m into it.</div>
                            </div>
                        </div>
                        <div class="moderatorbar">
                            <div class="smalltext modified" id="modified_3113180">
                            </div>
                            <div class="smalltext reportlinks">
                                <a href="https://geekhack.org/index.php?action=reporttm;topic=115887.44;msg=3113180">Report to moderator</a> &nbsp;
                                <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/ip.gif" alt="" />
                                <a href="https://geekhack.org/index.php?action=helpadmin;help=see_member_ip" onclick="return reqWin(this.href);" class="help">Logged</a>
                            </div>
                            <div class="signature" id="msg_3113180_signature"><a href="https://geekhack.org/index.php?topic=116335.0" class="bbc_link" target="_blank"> <img src="https://i.imgur.com/Wo07N3B.jpeg" alt="" width="254" height="110" align="" class="bbc_img resized" /> </a></div>
                        </div>
                    </div>
                    <span class="botslice"><span></span></span>
                </div>
                <hr class="post_separator" />
                </form>
            </div>
            <a id="lastPost"></a>
            <div class="pagesection">
                
        <div class="buttonlist floatright">
            <ul>
                <li><a class="button_strip_reply active" href="https://geekhack.org/index.php?action=post;topic=115887.0;last_msg=3113180"><span>Reply</span></a></li>
                <li><a class="button_strip_watch" href="https://geekhack.org/index.php?action=unwatch;topic=115887.0;b1b588e33=749de156f0789523e77cbbc9ade2366d"><span>Unwatch</span></a></li>
                <li><a class="button_strip_notify" href="https://geekhack.org/index.php?action=notify;sa=off;topic=115887.0;b1b588e33=749de156f0789523e77cbbc9ade2366d" onclick="return confirm('Are you sure you wish to disable notification of new replies for this topic?');"><span>Unnotify</span></a></li>
                <li><a class="button_strip_mark_unread" href="https://geekhack.org/index.php?action=markasread;sa=topic;t=3113185;topic=115887.0;b1b588e33=749de156f0789523e77cbbc9ade2366d"><span>Mark unread</span></a></li>
                <li><a class="button_strip_send" href="https://geekhack.org/index.php?action=emailuser;sa=sendtopic;topic=115887.0"><span>Send this topic</span></a></li>
                <li><a class="button_strip_print" href="https://geekhack.org/index.php?action=printpage;topic=115887.0" rel="new_win nofollow"><span class="last">Print</span></a></li>
            </ul>
        </div>
                <div class="pagelinks floatleft">Pages: &nbsp;[<strong>1</strong>] &nbsp;  &nbsp;&nbsp;<a href="#top"><strong>Go Up</strong></a></div>
                <div class="nextlinks_bottom"><a href="https://geekhack.org/index.php?topic=115887.0;prev_next=prev#new">&laquo; previous</a> <a href="https://geekhack.org/index.php?topic=115887.0;prev_next=next#new">next &raquo;</a></div>
            </div>
    <div class="navigate_section">
        <ul>
            <li>
                <a href="https://geekhack.org/index.php"><span>geekhack</span></a> &#187;
            </li>
            <li>
                <a href="https://geekhack.org/index.php#c49"><span>geekhack Marketplace</span></a> &#187;
            </li>
            <li>
                <a href="https://geekhack.org/index.php?board=132.0"><span>Interest Checks</span></a> (Moderator: <a href="https://geekhack.org/index.php?action=profile;u=31271" title="Board Moderator">Signature</a>) &#187;
            </li>
            <li class="last">
                <a href="https://geekhack.org/index.php?topic=115887.0"><span>[IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing</span></a>
            </li>
        </ul>
    </div>
            <div id="moderationbuttons">
        <div class="buttonlist floatbottom" id="moderationbuttons_strip">
            <ul>
                <li><a class="button_strip_lock" href="https://geekhack.org/index.php?action=lock;topic=115887.0;b1b588e33=749de156f0789523e77cbbc9ade2366d"><span class="last">Lock topic</span></a></li>
            </ul>
        </div></div>
            <div class="plainbox" id="display_jump_to">&nbsp;</div>
            <a id="quickreply"></a>
            <div class="tborder" id="quickreplybox">
                <div class="cat_bar">
                    <h3 class="catbg">
                        <span class="ie6_header floatleft"><a href="javascript:oQuickReply.swap();">
                            <img src="https://cdn.geekhack.org/Themes/Nostalgia/images/expand.gif" alt="+" id="quickReplyExpand" class="icon" />
                        </a>
                        <a href="javascript:oQuickReply.swap();">Quick Reply</a>
                        </span>
                    </h3>
                </div>
                <div id="quickReplyOptions" style="display: none">
                    <span class="upperframe"><span></span></span>
                    <div class="roundframe">
                        <p class="smalltext lefttext">With <em>Quick-Reply</em> you can write a post when viewing a topic without loading a new page. You can still use bulletin board code and smileys as you would in a normal post.</p>
                        
                        
                        
                        <form action="https://geekhack.org/index.php?board=132;action=post2" method="post" accept-charset="ISO-8859-1" name="postmodify" id="postmodify" onsubmit="submitonce(this);" style="margin: 0;">
                            <input type="hidden" name="topic" value="115887" />
                            <input type="hidden" name="subject" value="Re: [IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing" />
                            <input type="hidden" name="icon" value="xx" />
                            <input type="hidden" name="from_qr" value="1" />
                            <input type="hidden" name="notify" value="1" />
                            <input type="hidden" name="not_approved" value="" />
                            <input type="hidden" name="goback" value="0" />
                            <input type="hidden" name="last_msg" value="3113180" />
                            <input type="hidden" name="b1b588e33" value="749de156f0789523e77cbbc9ade2366d" />
                            <input type="hidden" name="seqnum" value="6505394" />
                            <div class="quickReplyContent">
                                <textarea cols="600" rows="7" name="message" tabindex="1"></textarea>
                            </div>
                            <div class="righttext padding">
                                <input type="submit" name="post" value="Post" onclick="return submitThisOnce(this);" accesskey="s" tabindex="2" class="button_submit" />
                                <input type="submit" name="preview" value="Preview" onclick="return submitThisOnce(this);" accesskey="p" tabindex="3" class="button_submit" />
                            </div>
                        </form>
                    </div>
                    <span class="lowerframe"><span></span></span>
                </div>
            </div>
                <script type="text/javascript" src="https://cdn.geekhack.org/Themes/default/scripts/topic.js"></script>
                <script type="text/javascript"><!-- // --><![CDATA[
                    var oQuickReply = new QuickReply({
                        bDefaultCollapsed: true,
                        iTopicId: 115887,
                        iStart: 0,
                        sScriptUrl: smf_scripturl,
                        sImagesUrl: "https://cdn.geekhack.org/Themes/Nostalgia/images",
                        sContainerId: "quickReplyOptions",
                        sImageId: "quickReplyExpand",
                        sImageCollapsed: "collapse.gif",
                        sImageExpanded: "expand.gif",
                        sJumpAnchor: "quickreply"
                    });
                    if ('XMLHttpRequest' in window)
                    {
                        var oQuickModify = new QuickModify({
                            sScriptUrl: smf_scripturl,
                            bShowModify: true,
                            iTopicId: 115887,
                            sTemplateBodyEdit: '\n\t\t\t\t\t\t\t\t<div id="quick_edit_body_container" style="width: 90%">\n\t\t\t\t\t\t\t\t\t<div id="error_box" style="padding: 4px;" class="error"><' + '/div>\n\t\t\t\t\t\t\t\t\t<textarea class="editor" name="message" rows="12" style="width: 100%; margin-bottom: 10px;" tabindex="4">%body%<' + '/textarea><br />\n\t\t\t\t\t\t\t\t\t<input type="hidden" name="b1b588e33" value="749de156f0789523e77cbbc9ade2366d" />\n\t\t\t\t\t\t\t\t\t<input type="hidden" name="topic" value="115887" />\n\t\t\t\t\t\t\t\t\t<input type="hidden" name="msg" value="%msg_id%" />\n\t\t\t\t\t\t\t\t\t<div class="righttext">\n\t\t\t\t\t\t\t\t\t\t<input type="submit" name="post" value="Save" tabindex="5" onclick="return oQuickModify.modifySave(\'749de156f0789523e77cbbc9ade2366d\', \'b1b588e33\');" accesskey="s" class="button_submit" />&nbsp;&nbsp;<input type="submit" name="cancel" value="Cancel" tabindex="6" onclick="return oQuickModify.modifyCancel();" class="button_submit" />\n\t\t\t\t\t\t\t\t\t<' + '/div>\n\t\t\t\t\t\t\t\t<' + '/div>',
                            sTemplateSubjectEdit: '<input type="text" style="width: 90%;" name="subject" value="%subject%" size="80" maxlength="80" tabindex="7" class="input_text" />',
                            sTemplateBodyNormal: '%body%',
                            sTemplateSubjectNormal: '<a hr'+'ef="https://geekhack.org/index.php'+'?topic=115887.msg%msg_id%#msg%msg_id%" rel="nofollow">%subject%<' + '/a>',
                            sTemplateTopSubject: 'Topic: %subject% &nbsp;(Read 10220 times)',
                            sErrorBorderStyle: '1px solid red'
                        });

                        aJumpTo[aJumpTo.length] = new JumpTo({
                            sContainerId: "display_jump_to",
                            sJumpToTemplate: "<label class=\"smalltext\" for=\"%select_id%\">Jump to:<" + "/label> %dropdown_list%",
                            iCurBoardId: 132,
                            iCurBoardChildLevel: 0,
                            sCurBoardName: "Interest Checks",
                            sBoardChildLevelIndicator: "==",
                            sBoardPrefix: "=> ",
                            sCatSeparator: "-----------------------------",
                            sCatPrefix: "",
                            sGoButtonLabel: "go"
                        });

                        aIconLists[aIconLists.length] = new IconList({
                            sBackReference: "aIconLists[" + aIconLists.length + "]",
                            sIconIdPrefix: "msg_icon_",
                            sScriptUrl: smf_scripturl,
                            bShowModify: true,
                            iBoardId: 132,
                            iTopicId: 115887,
                            sSessionId: "749de156f0789523e77cbbc9ade2366d",
                            sSessionVar: "b1b588e33",
                            sLabelIconList: "Message Icon",
                            sBoxBackground: "transparent",
                            sBoxBackgroundHover: "#ffffff",
                            iBoxBorderWidthHover: 1,
                            sBoxBorderColorHover: "#adadad" ,
                            sContainerBackground: "#ffffff",
                            sContainerBorder: "1px solid #adadad",
                            sItemBorder: "1px solid #ffffff",
                            sItemBorderHover: "1px dotted gray",
                            sItemBackground: "transparent",
                            sItemBackgroundHover: "#e0e0f0"
                        });
                    }
            function mquote(msg_id,remove)
            {
                if (!window.XMLHttpRequest)
                    return true;

                var elementButton = "mquote_" + msg_id;
                var elementButtonDelete = "mquote_remove_" + msg_id;
                var exdate = new Date();
                (remove == "remove") ? exdate.setDate(exdate.getDate() - 1) : exdate.setDate(exdate.getDate() + 1);
                document.getElementById(elementButton).style.display = (remove == "remove") ? "inline" : "none";
                document.getElementById(elementButtonDelete).style.display = (remove == "remove") ? "none" : "inline";
                document.cookie = "mquote" + msg_id + "=; expires="+exdate.toGMTString()+"; path=/";
            }
                // ]]></script>
        </div>
    </div></div>
    <div id="footer_section"><div class="frame">
        <ul class="reset">
            <li class="copyright">
            <span class="smalltext" style="display: inline; visibility: visible; font-family: Verdana, Arial, sans-serif;"><a href="https://geekhack.org/index.php?action=credits" title="Simple Machines Forum" target="_blank" class="new_win">SMF 2.0.15.10
</a> |
 <a href="http://www.simplemachines.org/about/smf/license.php" title="License" target="_blank" class="new_win">SMF &copy; 2017</a>, <a href="http://www.simplemachines.org" title="Simple Machines" target="_blank" class="new_win">Simple Machines</a>
            </span></li>
            <li><a id="button_xhtml" href="http://validator.w3.org/check?uri=referer" target="_blank" class="new_win" title="Valid XHTML 1.0!"><span>XHTML</span></a></li>
            <li><a id="button_rss" href="https://geekhack.org/index.php?action=.xml;type=rss" class="new_win"><span>RSS</span></a></li>
            <li class="last"><a id="button_wap2" href="https://geekhack.org/index.php?wap2" class="new_win"><span>WAP2</span></a></li>
        </ul>
        <p>Page created in 0.215 seconds with 64 queries.</p>
    </div></div>
</div>
<!-- HS-4-SMF -->
<script type="text/javascript" src="https://cdn.geekhack.org/Themes/default/hs4smf/highslide.js"></script>
<script type="text/javascript"><!-- // --><![CDATA[
hs.graphicsDir = 'https://cdn.geekhack.org/Themes/default/hs4smf/graphics/';
hs.showCredits = false;
hs.fadeInOut = true;
hs.transitions = ['expand', 'crossfade'];
hs.align = 'center';
hs.padToMinWidth = true;
hs.lang = {
cssDirection:'ltr',
loadingText:'Loading...',
loadingTitle:'Click to cancel',
focusTitle:'Click to bring to front',
fullExpandTitle:'Expand to actual size',
creditsText:'Powered by <i>Highslide JS</i>',
creditsTitle:'Go to the Highslide JS homepage',
previousText:'Previous',
nextText:'Next',
moveText:'Move',
closeText:'Close',
closeTitle:'Close (esc)',
resizeTitle:'Resize',
playText:'Play',
playTitle:'Play slideshow (spacebar)',
pauseText:'Pause',
pauseTitle:'Pause slideshow (spacebar)',
previousTitle:'Previous (arrow left)',
nextTitle:'Next (arrow right)',
moveTitle:'Move',
fullExpandText:'Full size',
number:'Image %1 of %2',
restoreTitle:'Click to close image, click and drag to move. Use arrow keys for next and previous.',
};hs.captionEval = 'if (this.slideshowGroup == "aeva") {this.highslide-caption} else {"[IC] Calla - Seamless Side Profile F13 TKL w/ reduced switch spacing"} ';
hs.captionOverlay.position = 'below';
hs.captionOverlay.width = '100%';
hs.headingOverlay.width = '100%';
hs.captionOverlay.hideOnMouseOut = true;
hs.headingOverlay.hideOnMouseOut = true;
hs.captionOverlay.opacity = 0.9;
hs.headingOverlay.opacity = 0.9;
hs.outlineType = 'rounded-white';
hs.dimmingOpacity = 0.3;
hs.wrapperClassName = 'controls-in-heading';
// ]]></script>

</body></html>"""
    soup = BeautifulSoup(content2, 'html.parser')
    message_list = list()
    test = MessageScraper('https://geekhack.org/index.php?topic=115887.0', 'most_recent_post_ID.txt')
    #soup = BeautifulSoup(html_content, 'html.parser')
    '''
    for post in soup.find_all('div', attrs={'class':'postarea'}):
        why = post.find('div', attrs = {'class':'inner'})
        print(why)
        testttt = test.manage_quotes(why)
        if testttt[0] is not None:
            print('\n'.join(testttt[0]))
    '''
    test.update_post()
    message_list = test.repost_message()
    for message in message_list:
        print(message)
    
    '''
    why = soup.find('div', attrs = {'class':'inner'})
    headers = list()
    for message in soup.find_all('div', attrs={'class':"quoteheader"}):
        headers.append(message.text)
    for line_break in soup.find_all('br'):
        line_break.replace_with(' ')
    soup = BeautifulSoup(str(soup), 'html.parser')
    #print(soup.prettify())
    #print(headers)
    print(soup.find_all('blockquote', attrs={'class':"bbc_standard_quote"}))
    quotes = list(quote for quote in soup.find('blockquote', attrs={'class':"bbc_standard_quote"}).get_text('&&&&').split('&&&&') if not quote.startswith('Quote from:'))
    #print(quotes)
    print(test.manage_quotes(why))
    '''
    
    

          
    