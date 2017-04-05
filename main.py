from utils import *

def main():
    #answer_urls = './batch2_story_answer_urls.txt'
    #html_path = './second_batch2_answer_html/'
    #plain_text_path = './second_batch2_plain_text3/'
    answer_urls = './story_answer_urls.txt'
    html_path = './second_answer_html/'
    plain_text_path = './second_plain_text3/'
    #saveAnswers(answer_urls, html_path, plain_text_path, 19379)
    saveAttributes(html_path)
	
if __name__ == "__main__":
    main()
