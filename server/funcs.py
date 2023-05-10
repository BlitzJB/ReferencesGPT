import requests
from bs4 import BeautifulSoup
import openai
import os
import time
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())

openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_google_search_results(url):
    response = requests.get(url)
    open('google.html', 'wb').write(response.content)
    soup = BeautifulSoup(response.text, 'html.parser')
    outer_container = soup.find('div', id='main')
    inner_divs = outer_container.find_all('div')[3::]
    results = []
    for div in inner_divs:
        if div.find('h3') and div.find('a') and div.find('span'):
            results.append({
                'title': div.find('h3').text,
                'link': div.find('a')['href'],
                'description': div.find_all('span')[0].parent.text
            })
    titles = set()
    for result in results:
        if result['title'] not in titles:
            titles.add(result['title'])
    out = []
    for title in titles:
        for result in results:
            if result['title'] == title:
                out.append(result)
                break
    return out



def get_to_google_urls(input_text: str):
    payload = [
        {"role": "system", "content": "You are a researcher whos job is to purely generate atleast 3 google search query urls and their search intent which would give references for the provided text. You must stick to the format in the example and never include other prose. You must stick to only generating references to what is provided in the text and not go beyond. you must never repeat urls, but you can go beyond 3 if you find relevant urls."},
        {"role": "user", "content": """This report presents the findings of a survey on Artificial Intelligence (AI) which aimed to gauge public awareness, trust, fears, and beliefs about the impact of AI on the job market and human intelligence. The survey results revealed that while most participants were familiar with AI, there were varying levels of trust and fears about the technology. Participants also held divergent views on the impact of AI on job markets and its potential to surpass human intelligence. The report highlights the need for continued public education and engagement to better understand the potential impacts and benefits of AI.\nIn addition to the findings mentioned above, the survey also presented participants with two paragraphs, one advocating for the benefits of AI and the other highlighting potential risks and drawbacks. The survey then compared how participants' responses to the questions changed after reading each paragraph. The analysis showed that the presentation of these opposing viewpoints had a significant impact on participants' perceptions of AI. For example, those who initially expressed fear about AI were more likely to trust the technology after reading the paragraph advocating its benefits, while those who initially trusted AI were more likely to express concerns after reading the paragraph outlining its potential risks. These results suggest that balanced and nuanced discussions of AI are necessary for informed public dialogue about the technology.\nThe four parts of this report will cover (1) An overview of the responses received and how the survey was conducted,  (2) Comparing responses received without reinforcement for AI with responses after positive reinforcement for AI, (3) Comparing responses received without reinforcement against AI with responses after negative reinforcement of AI, and (4) Finding the number of people who have either changed their answer or have decided to maintain their chosen option."""},
        {"role": "assistant", "content": "https://www.google.com/search?q=Public+Views+on+AI%3A+Fearful+of+Losing+Jobs%2C+Want+Robots+to+Do+More+in+Caregiving**to understand how people think robots would replace them****https://www.google.com/search?q=AI+Now+2019+Report**get authentic statistics on AI****https://www.google.com/search?q=Europeans%27+attitudes+towards+AI**explore Europeans' attitudes towards AI****https://www.google.com/search?q=Edelman+Trust+Barometer%3A+Trust+in+Technology**trust in technology****https://www.google.com/search?q=PwC%3A+Sizing+the+prize%3A+What%27s+the+real+value+of+AI+for+your+business+and+how+can+you+capitalise%3F**real value of AI for businesses****https://www.google.com/search?q=The+Malicious+Use+of+Artificial+Intelligence%3A+Forecasting%2C+Prevention%2C+and+Mitigation**risks of malicious AI use****https://www.google.com/search?q=The+Future+of+Jobs+Report+2020**future of jobs****https://www.google.com/search?q=Deloitte%3A+Human+Capital+Trends+2021%3A+The+social+enterprise+in+a+world+disrupted**human capital trends in a disrupted world****https://www.google.com/search?q=Trust+in+the+Age+of+AI%3A+Exploring+Public+Opinion+on+Artificial+Intelligence+in+the+EU**public opinion on AI in the EU"},
        {"role": "user", "content": input_text},
    ]
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=payload,
        max_tokens=2000,
    )
    # return completion.choices[0].message
    return list(map(lambda x: {"url": x.split("**")[0], "intent": x.split("**")[1]},completion.choices[0].message.content.split("****")))

def select_urls_from_search(intent: str, results: list):
    while True:
        if (len(str(results)) > 8000):
            print("too long")
            results = results[:-1]
        else:
            break
    payload = [
        {"role": "system", "content": """You are a researcher and job is to pick out the urls which are the msot relevant to the given search intent. you are provided with the search intent as well as the search results. You must judge if the search result is relevant or not based on the description and the title. do not return all the urls that are provided, instead only set in urls that you are very sure is relevant. If multiple urls are relevant, boil down to the best. Never include any other prose other than the python list itself. the python list should be of the format [{"title": str, "description": str, "link":str}, ...]. Make sure to cleanup out of place characters like \xa0 and also remove unnecessary query or path params form urls"""},
        {"role": "user", "content": """Intent: Impact of blockchain on web development in 2021 and beyond. [{'description': '15-Apr-2020 · Blockchain integration into web development ' 'has successfully changed corporate communities faster than ' 'anticipated. Numerous industry titans in\xa0...', 'link': '/url?q=https://www.yashaaglobal.com/blog/how-blockchain-technology-can-impact-web-development/&sa=U&ved=2ahUKEwjslLq-mub-AhWSa2wGHZQEBtAQFnoECAMQAg&usg=AOvVaw035DBppOO5q5_cnmuKqclT', 'title': 'The Impact Of Blockchain Technology On The Web Development ...'}, {'description': "15-May-2021 · Blockchain has made an impact on today's " 'technology by revolutionizing the financial industry through ' 'utilization of cryptocurrencies using\xa0...', 'link': '/url?q=https://link.springer.com/article/10.1007/s10586-021-03301-8&sa=U&ved=2ahUKEwjslLq-mub-AhWSa2wGHZQEBtAQFnoECAkQAg&usg=AOvVaw3NPFGVb_OWgfjrD_qbyUlt', 'title': 'Blockchain for decentralization of internet: prospects, trends, ' 'and ...'}, {'description': '13-Jun-2021 · Bot€™s rise will make advent changes in ' 'website design, user experience. The important top-notch ' 'technology helps custom web development\xa0...', 'link': '/url?q=https://www.datasciencecentral.com/how-new-technology-trends-impact-web-development-in-2021/&sa=U&ved=2ahUKEwjslLq-mub-AhWSa2wGHZQEBtAQFnoECAAQAg&usg=AOvVaw3w-bSeKgH9rjCf-jr2ZkDU', 'title': 'How New Technology Trends Impact Web Development in 2021'}, {'description': '18-Oct-2021 · Creation of More Interactive Websites ... One ' 'of the primary aspects of blockchain is being very ' 'interactive. This means that when blockchain and\xa0...', 'link': '/url?q=https://webwolf.in/blog/how-use-of-blockchain-can-impact-web-development&sa=U&ved=2ahUKEwjslLq-mub-AhWSa2wGHZQEBtAQFnoECAQQAg&usg=AOvVaw0xHqpRCUp4n_3i1Jpu8q8n', 'title': 'How use of Blockchain can impact Web Development - Web Wolf'}]"""},
        {"role": "assistant", "content": "[{'title': 'How New Technology Trends Impact Web Development in 2021', 'description': 'Bot€™s rise will make advent changes in website design, user experience. The important top-notch technology helps custom web development...', 'link': 'https://www.datasciencecentral.com/how-new-technology-trends-impact-web-development-in-2021/'}, {'title': 'How use of Blockchain can impact Web Development - Web Wolf', 'description': 'Creation of More Interactive Websites ... One of the primary aspects of blockchain is being very interactive. This means that when blockchain and...', 'link': 'https://webwolf.in/blog/how-use-of-blockchain-can-impact-web-development'}]"},
        {"role": "user", "content": f"""Intent: {intent}\n{str(results)}"""},
    ]
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=payload,
        max_tokens=2000,
    )
    return eval(completion.choices[0].message.content)


def exec_function_for_n_tries(func, n, *args, **kwargs):
    for i in range(n):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Failed to execute function {func.__name__} {e}, trying again {i+1}/{n}")
            time.sleep(1)
    raise Exception("Failed to execute function")

def research(text: str):
    print("[STEP] Figuring out what to search")
    to_search = exec_function_for_n_tries(get_to_google_urls, 3, text)
    time.sleep(18)
    results = []
    print("[STEP] Googling!")
    for index, search in enumerate(to_search):
        print(f"[STEP] Searching for {search['intent']}")
        urls = exec_function_for_n_tries(get_google_search_results, 3, search["url"])
        print(f"[STEP] Seleting the best results")
        selected = exec_function_for_n_tries(select_urls_from_search, 3, search["intent"], urls)
        results.append({"intent": search["intent"], "results": selected})
        if index < len(to_search) - 1:
            print(f"[STEP] Sleeping because too poor to pay for openai")
            time.sleep(18)
    print("[STEP] Done!")
    return results
