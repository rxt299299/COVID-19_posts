# COVID-19_posts
posts about COVID-19 from December 2023

# API Endpoint Documentation:
## Endpoint URL:
http://127.0.0.1:5000/quesion5/{hashtag_name}
## Method:
- GET
## Expected Input Format:
- The input parameter should be a string representing the hashtag name.
- **diedsuddenly** in the given example (do not need starts with #)
- The endpoint URL for the above example would be: http://127.0.0.1:5000/quesion5/diedsuddenly

## Example of the Request Body (if applicable):
- As the input parameter is part of the URL, no request body example is needed.

## Structure of the Response:
- The response will be a JSON object containing the results of Question 5.
- Example Response:
```json
{
  'result':{'Q1':[["#Pfizer",18249],["#DiedSuddenly",10403],["#Moderna",10247],["#ableg",10078],["#cdnpoli",10053]],
            'Q2':66,
            'Q3':37,
            'Q4':34
            },
  'description':{
      'Q1': 'The 5 most commonly used hashtags and the number of times they were each used.',
      'Q2':'Count of unique pairs of original posts used the hashtag #diedsuddenly and were posted within 10 seconds of one another',
      'Q3':'Count of unique pairs of the accounts posted #diedsuddenly and have screen names with a similarity greater than 0.8',
      'Q4':'Unique pairs of accounts both synchronously posted the hashtag #diedsuddenly and have similar screen names'
  }
    }
```
