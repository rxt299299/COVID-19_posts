import pandas as pd
from collections import *
from rapidfuzz.distance.DamerauLevenshtein import normalized_similarity
import os
#!pip install rapidfuzz


root_dir = os.path.dirname(os.path.abspath(__file__))
post_path = os.path.join(root_dir, 'data/posts.tsv')
account_path = os.path.join(root_dir, 'data/accounts.tsv')


def load_data(post_path, account_path):
    #load the posts and accounts into panads dataframe
    df_post = pd.read_csv(post_path, sep='\t', lineterminator='\n')
    df_account = pd.read_csv(account_path, sep='\t', lineterminator='\n')
    return df_post, df_account


def question_1(df_post):
    ###########
    #question 1
    #define a dictionary where the key is hastag and value is the count of hashtag showed in all posts
    hashtag_cnt_dict = defaultdict(int)
    for _, row in df_post.iterrows():
        #some line is blank ('nan')
        if pd.notna(row['hashtags']):
            hashtags = str(row["hashtags"]).split('|')
            for hashtag in hashtags:
                hashtag_cnt_dict[hashtag]+=1

    # #assume each hashtag should be started with '#'
    # #let's check if there exists some outliers
    # for hastag in hashtag_cnt_dict.keys():
    #     if not hashtag.startswith('#'):
    #         print (hashtag, hashtag_cnt_dict[hashtag])

    #print nothing here. Great, all hashtag starts with '#'

    #get the 5 most commonly used hashtags and their used times
    hashtag_cnts_top5 = sorted(hashtag_cnt_dict.items(), key=lambda x:x[1], reverse=True)[:5]
    print ('the 5 most commonly used hashtags and the number of times they were each used.')
    print (hashtag_cnts_top5)
    return hashtag_cnts_top5

###########
#question 2
#define a function detect if the row exists the hashtag_name hashtag
def hashtag_exist(row_hashtags, hashtag_name):
  hashtags = row_hashtags.split('|')
  if hashtag_name in hashtags:
    return True
  return False

def question_2(df_post, hashtag_name):
    #filter out the reposts
    df_post_original = df_post[df_post['is_repost']==False]
    #drop the rows with blank hastags
    df_post_original = df_post_original.dropna(subset=['hashtags'])
    #set a new column named if_hashtag, if the hashtags has #diedsuddenly, the column is True else False
    df_post_original['if_hashtag'] = df_post_original.apply(lambda row: hashtag_exist(row.hashtags, hashtag_name), axis=1)

    #extract all the timestamps where this post has the #diedsuddenly and run sorted
    time_posts_list = df_post_original[df_post_original['if_hashtag']]['created_at'].tolist()
    #convert the type to datetime for calculations in next step
    time_posts_list = [pd.to_datetime(item, format='%Y-%m-%d %H:%M:%S.%f') for item in time_posts_list]

    #sorted the convert time
    author_id_list = df_post_original[df_post_original['if_hashtag']]['author_id'].tolist()

    time_posts_author_id_list = list(zip(time_posts_list, author_id_list))
    time_posts_author_id_list = sorted(time_posts_author_id_list, key=lambda x:x[0])

    #get the #cnt of the pairs
    synchronous_post_pair_cnts = 0
    synchronous_post_author_id_pairs = []

    #for each timespot try to compare with timespot bigger than it
    #do not need to compare with timespot smaller than it
    #since pairs are bidirectional, pairs with timespot smaller than it have already been compared.
    for i in range(len(time_posts_author_id_list)):
        for j in range(i+1, len(time_posts_author_id_list)):

            time_1, author_id_1 = time_posts_author_id_list[i]
            time_2, author_id_2 = time_posts_author_id_list[j]
            if time_2<=time_1 + pd.Timedelta(seconds=10):
                #print (time_posts_list[i], '|', time_posts_list[j])
                synchronous_post_pair_cnts+=1
                #get the pairs of author_ids
                author_pairs = tuple(sorted([author_id_1, author_id_2]))
                if author_pairs not in synchronous_post_author_id_pairs:
                    synchronous_post_author_id_pairs.append(author_pairs)
            else:
                #since the time_posts_list is sorted, if difference >10s for j, we do not need to compare index bigger than j
                break


    print ("Count of unique pairs of original posts used the hashtag #diedsuddenly and were posted within 10 seconds of one another")
    print (synchronous_post_pair_cnts)
    return synchronous_post_pair_cnts, synchronous_post_author_id_pairs, df_post_original

###########
#question 3
def question_3(df_post_original, df_account):
    #get the list of author_id and screen_name where they had posts with tag #diedsuddenly and not repost
    unique_author_ids = set(df_post_original[df_post_original['if_hashtag']]['author_id'].tolist())
    author_ids = df_account[df_account['id'].isin(unique_author_ids)]['id'].tolist()
    screen_names = df_account[df_account['id'].isin(unique_author_ids)]['screen_name'].tolist()


    similar_screen_name_pairs_cnt = 0
    similar_screen_name_author_id_pairs = []

    for i in range(len(author_ids)):
        for j in range(i+1, len(author_ids)):
            #get the similarity score between two screen names
            similarity_score = normalized_similarity(screen_names[i], screen_names[j])
            if similarity_score>0.8:
                #print (similarity_score, scree_name_1, scree_name_2)
                similar_screen_name_pairs_cnt+=1

                #get the pairs of author_ids
                author_pairs = tuple(sorted([author_ids[i], author_ids[j]]))
                if author_pairs not in similar_screen_name_author_id_pairs:
                    similar_screen_name_author_id_pairs.append(author_pairs)

    print ("Count of unique pairs of the accounts posted #diedsuddenly and have screen names with a similarity greater than 0.8")
    print (similar_screen_name_pairs_cnt)
    return similar_screen_name_pairs_cnt, similar_screen_name_author_id_pairs


###########
#question 4
def question_4(synchronous_post_author_id_pairs, similar_screen_name_author_id_pairs):
    overlap_cnts = 0
    for item in synchronous_post_author_id_pairs:
        if item in similar_screen_name_author_id_pairs:
            overlap_cnts+=1

    print ('unique pairs of accounts both synchronously posted the hashtag #diedsuddenly and have similar screen names')
    print (overlap_cnts)
    return overlap_cnts

def main(hashtag_name):
    #hashtag_name = '#diedsuddenly' in this example
    #load data
    df_post, df_account = load_data(post_path, account_path)
    #run question from 1 to 4
    hashtag_cnts_top5 = question_1(df_post)
    synchronous_post_pair_cnts, synchronous_post_author_id_pairs, df_post_original = question_2(df_post, hashtag_name)
    similar_screen_name_pairs_cnt, similar_screen_name_author_id_pairs = question_3(df_post_original, df_account)
    overlap_cnts = question_4(synchronous_post_author_id_pairs, similar_screen_name_author_id_pairs)

    # output_result = {
    # 'Q1':{'result':hashtag_cnts_top5,
    #         'description':'the 5 most commonly used hashtags and the number of times they were each used.'},
    # 'Q2':{'result':synchronous_post_pair_cnts,
    #         'description':'Count of unique pairs of original posts used the hashtag #diedsuddenly and were posted within 10 seconds of one another'},
    # 'Q3':{'result':similar_screen_name_pairs_cnt,
    #         'description':'Count of unique pairs of the accounts posted #diedsuddenly and have screen names with a similarity greater than 0.8'},
    # 'Q4':{'result':overlap_cnts,
    #         'description':'unique pairs of accounts both synchronously posted the hashtag #diedsuddenly and have similar screen names'}

    # }   

    output_result = {
        'result':{'Q1':hashtag_cnts_top5,
                  'Q2':synchronous_post_pair_cnts,
                  'Q3':similar_screen_name_pairs_cnt,
                  'Q4':overlap_cnts
                  },
        'description':{
            'Q1': 'the 5 most commonly used hashtags and the number of times they were each used.',
            'Q2':'Count of unique pairs of original posts used the hashtag #diedsuddenly and were posted within 10 seconds of one another',
            'Q3':'Count of unique pairs of the accounts posted #diedsuddenly and have screen names with a similarity greater than 0.8',
            'Q4':'unique pairs of accounts both synchronously posted the hashtag #diedsuddenly and have similar screen names'
        }
    }

    return output_result

