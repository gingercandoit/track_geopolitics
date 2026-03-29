# RSS Feed Research Results — Geopolitics Tracking Project

> Generated: 2026-03-28
> Method: Programmatic testing with `feedparser` + `urllib` (4 rounds, ~100 URLs tested)
> Notes: "Needs UA" = requires browser-like `User-Agent` header. Content quality rated by feedparser fields.

---

## A-Tier: Government Sources

| Source | Feed URL | Entries | Content Quality | Notes |
|--------|----------|---------|----------------|-------|
| **White House — All News** | `https://www.whitehouse.gov/news/feed/` | 10 | Summary + Full HTML | Excellent. Full `content:encoded` with complete article text |
| **White House — Presidential Actions** | `https://www.whitehouse.gov/presidential-actions/feed/` | 10 | Summary + Full HTML | Executive orders, proclamations. Full text included |
| **White House — Briefings** | `https://www.whitehouse.gov/briefings-statements/feed/` | 10 | Summary + Full HTML | Press briefings, statements |
| **State Dept — Press Releases** | `https://www.state.gov/rss-feed/press-releases/feed/` | 10 | Summary + Full HTML | **Needs UA**. Works perfectly with User-Agent header |
| **State Dept — All Releases** | `https://www.state.gov/rss-feed/collected-department-releases/feed/` | 10 | Summary + Full HTML | **Needs UA** |
| **State Dept — Briefings** | `https://www.state.gov/rss-feed/department-press-briefings/feed/` | 10 | Summary + Full HTML | **Needs UA**. Less frequently updated (last: Nov 2025) |
| **UK FCDO** | `https://www.gov.uk/government/organisations/foreign-commonwealth-development-office.atom` | 20 | Summary only | Atom format. Travel advisories + policy statements |
| **Federal Reserve — All Press** | `https://www.federalreserve.gov/feeds/press_all.xml` | 20 | Summary only | FOMC statements, regulatory announcements |
| **Federal Reserve — Speeches** | `https://www.federalreserve.gov/feeds/speeches.xml` | 15 | Summary only | Governor/Chair speeches and remarks |
| **GAO — Reports** | `https://www.gao.gov/rss/reports.xml` | 25 | Summary only | Government accountability reports |
| **EIA — Press Releases** | `https://www.eia.gov/rss/press_rss.xml` | 4 | Summary only | US energy data releases. Low volume but high value |

### A-Tier: Confirmed NO Working RSS

| Source | Status | Notes |
|--------|--------|-------|
| USTR | 404 on all patterns | Old Drupal feed from 2009 exists but stale. No current feed |
| Treasury / OFAC | 404 | No RSS found across multiple URL patterns |
| Commerce BIS | 404 | No RSS found |
| European Commission | Returns HTML, not RSS | Press corner has no parseable feed |
| EU External Action (EEAS) | 404 | No RSS found |
| Xinhua / english.news.cn | Old feed stale (2018) | `xinhuanet.com` feed exists but last entry from Jan 2018 |
| Japan MOFA | 403 | Blocked |
| China MOFCOM | — | No English RSS found |

---

## B-Tier: International Organizations

| Source | Feed URL | Entries | Content Quality | Notes |
|--------|----------|---------|----------------|-------|
| **UN News — Peace & Security** | `https://news.un.org/feed/subscribe/en/news/topic/peace-and-security/feed/rss.xml` | 30 | Summary only | Active and relevant. Topic-specific feed |
| **WHO News** | `https://www.who.int/rss-feeds/news-english.xml` | 25 | Summary + Full HTML | Full articles included |
| **NBER — New Working Papers** | `https://www.nber.org/rss/new.xml` | 21 | Summary only | Academic papers, useful for economics research |

### B-Tier: Confirmed NO Working RSS

| Source | Status | Notes |
|--------|--------|-------|
| IMF | 403 Forbidden | Blocks all programmatic access |
| World Bank | SSL errors / HTML returns | No parseable feed found |
| WTO | Returns HTML (10KB) | Multiple URL patterns return web page, not feed |
| IEA | 404 | No RSS found |
| OECD | 403 Forbidden | Blocks all programmatic access |
| BIS (Bank for Intl Settlements) | 404 | Old RSS URLs are dead |
| UNCTAD | 404 | No RSS found |

---

## C-Tier: Major Media

| Source | Feed URL | Entries | Content Quality | Notes |
|--------|----------|---------|----------------|-------|
| **Bloomberg Politics** | `https://feeds.bloomberg.com/politics/news.rss` | 30 | Summary + Full HTML | Excellent. ~2-3 sentence summaries + full content |
| **Bloomberg Economics** | `https://feeds.bloomberg.com/economics/news.rss` | 30 | Summary + Full HTML | Same quality as Politics feed |
| **Bloomberg Technology** | `https://feeds.bloomberg.com/technology/news.rss` | 30 | Summary + Full HTML | Useful for tech/chip geopolitics |
| **WSJ World News** | `https://feeds.content.dowjones.io/public/rss/RSSWorldNews` | 75 | Summary only | High volume. 1-2 sentence summaries |
| **WSJ Business** | `https://feeds.content.dowjones.io/public/rss/WSJcomUSBusiness` | 85 | **Titles only** | No summaries — headlines only |
| **WSJ Markets** | `https://feeds.content.dowjones.io/public/rss/RSSMarketsMain` | 60 | Summary only | |
| **WSJ Opinion** | `https://feeds.content.dowjones.io/public/rss/RSSOpinion` | 19 | Summary only | Editorials and op-eds |
| **FT Home** | `https://www.ft.com/rss/home` | 10 | Summary only | Short summaries. Paywalled articles |
| **FT World** | `https://www.ft.com/world?format=rss` | 25 | Summary only | |
| **Economist International** | `https://www.economist.com/international/rss.xml` | 300 | Summary only | Very high volume. Also available by topic (see below) |
| **Economist Leaders** | `https://www.economist.com/leaders/rss.xml` | 300 | Summary only | Editorial leaders |
| **Economist Finance & Econ** | `https://www.economist.com/finance-and-economics/rss.xml` | 300 | Summary only | |
| **Economist Asia** | `https://www.economist.com/asia/rss.xml` | 300 | Summary only | |
| **Economist China** | `https://www.economist.com/china/rss.xml` | 300 | Summary only | |
| **Economist US** | `https://www.economist.com/united-states/rss.xml` | 300 | Summary only | |
| **NPR World** | `https://feeds.npr.org/1004/rss.xml` | 10 | Summary + Full HTML | Full article text included |
| **NPR Politics** | `https://feeds.npr.org/1014/rss.xml` | 10 | Summary + Full HTML | |
| **BBC World** | `http://feeds.bbci.co.uk/news/world/rss.xml` | 37 | Summary only | 1-2 sentence descriptions |
| **BBC Business** | `http://feeds.bbci.co.uk/news/business/rss.xml` | 54 | Summary only | |
| **CNBC World** | `https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100727362` | 30 | Summary only | |
| **CNBC Economy** | `https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258` | 30 | Summary only | |
| **Al Jazeera** | `https://www.aljazeera.com/xml/rss/all.xml` | 25 | Summary only | All topics combined |
| **Guardian World** | `https://www.theguardian.com/world/rss` | 45 | Summary only | |
| **Foreign Affairs** | `https://www.foreignaffairs.com/rss.xml` | 20 | Summary only | Paywalled articles |
| **Foreign Policy** | `https://foreignpolicy.com/feed/` | 25 | Summary + Full HTML | Good geopolitics coverage |
| **SCMP** | `https://www.scmp.com/rss/91/feed` | 50 | Summary only | South China Morning Post. Asia/China focused |
| **The Diplomat** | `https://thediplomat.com/feed/` | 96 | Summary only | Asia-Pacific focused |

### C-Tier: Media — Confirmed NO Working RSS

| Source | Status | Notes |
|--------|--------|-------|
| Reuters | Dead URLs / SSL errors | All known feed URLs are defunct |
| AP News | 400 Bad Request | No public RSS found |
| Nikkei Asia | 404 | No RSS found |
| S&P Global/Platts | 403 | Blocked |
| CGTN | 404 | No RSS found |

### C-Tier: Stale/Low-Value Feeds (Not Recommended)

| Source | Feed URL | Issue |
|--------|----------|-------|
| China Daily World | `https://www.chinadaily.com.cn/rss/world_rss.xml` | Last entry from **Dec 2017** — abandoned feed |
| Global Times | `https://www.globaltimes.cn/rss/outbrain.xml` | Titles only, no summaries. Sporadic updates |
| Xinhua (old domain) | `https://www.xinhuanet.com/english/rss/worldrss.xml` | Last entry from **Jan 2018** — stale |

---

## C-Tier: Think Tanks & Research

| Source | Feed URL | Entries | Content Quality | Notes |
|--------|----------|---------|----------------|-------|
| **War on the Rocks** | `https://warontherocks.com/feed/` | 100 | Summary only | Defense/security analysis. Very active |
| **Bruegel** | `https://www.bruegel.org/rss.xml` | 10 | Summary only | EU economic policy think tank |
| **East Asia Forum** | — | — | — | 403 Forbidden |

### Think Tanks: Confirmed NO Working RSS

| Source | Status | Notes |
|--------|--------|-------|
| PIIE | 403 Forbidden | Blocks all access |
| CSIS | 403/404 | Multiple URL patterns fail |
| CFR | 403 Forbidden | Blocks all access |
| Brookings | Returns HTML (~164KB) | Feed URLs return full web page, not RSS |
| Chatham House | 403 Forbidden | Blocks all access |
| Carnegie Endowment | Returns HTML (~74KB) | Feed URLs return web page, not RSS |
| RAND | Returns HTML (~106KB) | Feed URL returns web page, not RSS |
| VoxEU/CEPR | 403/404 | No working feed |
| Lawfare | 403 Forbidden | Blocks all access |

---

## Summary Statistics

| Category | Working Feeds | No RSS / Blocked |
|----------|--------------|-----------------|
| A-Tier (Government) | 11 | 8 |
| B-Tier (International Orgs) | 3 | 7 |
| C-Tier (Media) | 26 | 5 |
| C-Tier (Think Tanks) | 2 | 9 |
| **Total** | **42** | **29** |

---

## Recommendations for SOP Update

### High-Value Additions to SOP (not currently listed)

1. **NPR** — World + Politics feeds have full article text, completely free
2. **Foreign Policy** — Full articles via RSS, excellent geopolitics depth
3. **Foreign Affairs** — Summaries available (articles paywalled)
4. **SCMP** — Key Asia/China coverage
5. **The Diplomat** — Asia-Pacific policy analysis
6. **UN News** — Peace & Security topic feed active with good summaries
7. **Federal Reserve** — Press releases + speeches (relevant for economic policy tracking)
8. **EIA** — US Energy Information Agency data releases
9. **War on the Rocks** — Defense/security analysis

### SOP Corrections Needed

1. **Bloomberg Markets** feed (`https://feeds.bloomberg.com/markets/news.rss`) — listed in SOP but returns identical content to Politics/Economics feeds (same 30 entries). Appears to be a shared feed.
2. **Bloomberg Energy** feed — 404, does not exist
3. **Reuters RSS** — All old Reuters feed URLs are dead. Reuters no longer offers public RSS. Remove from SOP or note as "Exa search only"
4. **State Dept feeds** — Work but **require User-Agent header**. Must use `urllib` with UA, not bare `feedparser.parse(url)`
5. **WSJ Business** — Returns titles only (no summaries), lower value than other WSJ feeds

### Sources Requiring Alternative Access Methods

These important sources have no RSS and must be accessed via **Exa search** or **fetch_webpage**:
- USTR, Treasury/OFAC, Commerce BIS (A-tier government)
- IMF, World Bank, WTO, IEA, OECD (B-tier international orgs)
- PIIE, CSIS, CFR, Brookings, Chatham House, Carnegie (C-tier think tanks)

### Technical Notes

- **User-Agent required for**: State Dept feeds (returns 0 entries without UA)
- **SSL verification note**: Some sites (World Bank) have SSL issues; `ssl.CERT_NONE` context may help but feeds still return HTML
- **Economist volume**: 300 entries per topic feed — consider filtering by date or keyword
- **Reddit JSON API**: Already in SOP and confirmed working (separate from RSS testing)
