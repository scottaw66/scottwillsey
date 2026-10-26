+++
# Root section: posts live directly here (hand/script-authored TOML markdown;
# tools/prebuild.py maintains their [extra] display fields) so their URLs
# stay /{slug}. NOT paginated — / is the standalone homepage (index.html);
# list pages /1…/N are stubs tools/prebuild.py generates in
# content/listpages/, rendered by postlist.html.
sort_by = "date"
page_template = "post.html"
# Section feed at /rss.xml (posts only — site-wide generate_feeds stays off
# so reads/stubs don't leak in). templates/rss.xml matches the @astrojs/rss
# output; tools/postbuild.py applies the ultrahtml-equivalent transforms.
generate_feeds = true
+++
