# Nigerian News Channels RSS Feeds

## Introduction

RSS (Really Simple Syndication) feeds are a standardized format used to distribute updated information from websites, such as news sites, blogs, or podcasts. They allow users to subscribe to updates from various sources and receive new content automatically.

This repository is an attempt to collect and organize the RSS links of Nigerian local news channels in an easy-to-parse format. 

## Contributing

1. **Add Your Entry**: Here is an example of an entry:
    ```json
        {
            "id": 6,
            "name": "Daily Trust",
            "base": "https://dailytrust.com",
            "feed": "https://dailytrust.com/feed/",
            "info": {
                "type": "general", 
                "reputation": "medium", 
                "status": "live", 
                "latency": 12
                }

        },
    ```
   - `id`: A unique identifier for the news channel, continue from the last id entered.
   - `name`: The name of the news channel.
   - `base`: The base URL of the news channel's website.
   - `feed`: The URL of the RSS feed. If unavailable, set this to `null` .
   - `info`: An object containing additional information:
     - `type`: Type of source (e.g., general, sports).
     - `reputation`: Reputation level (this is categorials with values: high, medium and low).
     - `status`: Wheather link is alive or stale. Set it to anything, the validator will determine.
     - `latency`: Time taken to retrieve the feed. Set it to anything, the validator will determine.



2. **Validate Your Entry**: Run the `validate-sites.py` script to ensure that your entry does not introduce any issues. If the validation runs successfully and a `sites-validated.json` file is produced, you may submit a pull request with your changes to merge your contributions.

**Note**: Not all sites have RSS pages, in this case you have to scrape the base URL to find what you are looking for. And, the reputation here is not objective as it is assigned based on the percieved popularity. 

## Applications

- [Here](https://github.com/dmachinewhisperer/nigerian-news-channel-aggregator/) is a simple local news aggregator using the RSS feed links here. 
- I made a Kaggle notebook on how to run sentiment analysis on news items pulled from these feeds [here](link_to_kaggle_notebook).

## License
MIT License. You are free to use, modify, and distribute the content as you see fit.
