I submitted two plugins to SiYuan's plugin bazaar today and wanted to know what a normal start looks like. The bazaar index on GitHub has stars but no download counts. A running SiYuan has them, though: the app asks its own kernel for the store listing, and every package in the answer carries a `downloads` field. So I started a SiYuan 3.8.9 kernel on my server and asked it for all 637 plugins.

```
curl -s -X POST http://127.0.0.1:6806/api/bazaar/getBazaarPlugin \
  -d '{"frontend":"browser-desktop","keyword":""}'
```

I matched each plugin with the date it was added to the index (the `created` field in `stage/plugins.json` of [siyuan-note/bazaar](https://github.com/siyuan-note/bazaar)). Everything below comes from those two files, pulled on 7 November 2026.

## A new plugin gets about one download a day

| Age in the bazaar | Plugins | Median downloads | 75th percentile |
|---|---|---|---|
| under 2 weeks | 45 | 17 | 38 |
| 2 weeks to 6 weeks | 80 | 52.5 | 108 |
| 6 weeks to 4 months | 136 | 105.5 | 255 |
| 4 months to 13 months | 113 | 638 | 1,931 |
| older | 263 | 1,867 | 6,106 |

For plugins between one and four months old, the median is 1.3 downloads a day and the top tenth gets 7 or more. That's the realistic picture for a small utility: a few people a day find it in the in-app store and try it.

The fast starters are few and they're bigger tools. A CalDAV sync plugin reached 607 downloads in 34 days, an Excalidraw whiteboard 281 in 18 days, and a study-course plugin 170 in 9 days.

## The top ten plugins have a third of all downloads

The 637 plugins have 2,059,230 downloads between them. The ten biggest hold 32% of that, and the top 10% hold 73%. At the other end, 187 plugins have fewer than 100 downloads and 409 have fewer than 1,000. The leader, a productivity toolbox, has 152,033.

Stars follow downloads closely: the correlation between log stars and log downloads is 0.76. The median plugin has 1 star, so a single star already puts a plugin in the upper half.

## Half the bazaar arrived this year

339 of the 637 plugins were added in 2026. Through May, about 10 to 19 new plugins arrived each month. From July it was 50 to 80 a month, with 80 in October and 25 in the first week of November. June shows only one, which I can't explain from the index alone.

| Added | Plugins | Mention AI, LLMs or agents |
|---|---|---|
| 2023 | 101 | 2 |
| 2024 | 90 | 1 |
| 2025 | 107 | 8 |
| 2026 | 339 | 55 |

I counted "AI-related" with a keyword match on names and descriptions (AI, LLM, GPT, Claude, DeepSeek, agent, MCP, 大模型, 人工智能), so it's rough. Even so, one in six plugins added this year is about AI, against fewer than one in 25 (11 of 298) before.

For someone publishing now, this means a new plugin lands on the same day as two or three others. Being listed is easy; the review is mostly automated and merges in hours. Being found is the work.

## Chinese first, donations second

574 of the 637 plugins have a Chinese description, which matches who uses SiYuan. A plugin with only an English description is the exception.

236 plugins list a real donation link in their manifest. 99 of those point to Afdian (爱发电), the Chinese creator-support site. Ko-fi has 13, PayPal 5, and 21 use GitHub Sponsors. Paid tiers are rare: a handful of plugins sell activation codes by hand.

The download counts are what SiYuan's store reports, which may include reinstalls and updates; I can't tell them apart from new users. My own two plugins were submitted today, [Notification History](https://github.com/prometheus-maker/siyuan-notification-history) and [Sticky Doc Tree](https://github.com/prometheus-maker/siyuan-sticky-doc-tree), so in two weeks I'll know whether they beat 17.
