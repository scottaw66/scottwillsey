declare module 'astro:content' {
	interface Render {
		'.md': Promise<{
			Content: import('astro').MarkdownInstance<{}>['Content'];
			headings: import('astro').MarkdownHeading[];
			remarkPluginFrontmatter: Record<string, any>;
		}>;
	}
}

declare module 'astro:content' {
	type Flatten<T> = T extends { [K: string]: infer U } ? U : never;

	export type CollectionKey = keyof AnyEntryMap;
	export type CollectionEntry<C extends CollectionKey> = Flatten<AnyEntryMap[C]>;

	export type ContentCollectionKey = keyof ContentEntryMap;
	export type DataCollectionKey = keyof DataEntryMap;

	type AllValuesOf<T> = T extends any ? T[keyof T] : never;
	type ValidContentEntrySlug<C extends keyof ContentEntryMap> = AllValuesOf<
		ContentEntryMap[C]
	>['slug'];

	export function getEntryBySlug<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(
		collection: C,
		// Note that this has to accept a regular string too, for SSR
		entrySlug: E
	): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;

	export function getDataEntryById<C extends keyof DataEntryMap, E extends keyof DataEntryMap[C]>(
		collection: C,
		entryId: E
	): Promise<CollectionEntry<C>>;

	export function getCollection<C extends keyof AnyEntryMap, E extends CollectionEntry<C>>(
		collection: C,
		filter?: (entry: CollectionEntry<C>) => entry is E
	): Promise<E[]>;
	export function getCollection<C extends keyof AnyEntryMap>(
		collection: C,
		filter?: (entry: CollectionEntry<C>) => unknown
	): Promise<CollectionEntry<C>[]>;

	export function getEntry<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(entry: {
		collection: C;
		slug: E;
	}): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof DataEntryMap,
		E extends keyof DataEntryMap[C] | (string & {}),
	>(entry: {
		collection: C;
		id: E;
	}): E extends keyof DataEntryMap[C]
		? Promise<DataEntryMap[C][E]>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(
		collection: C,
		slug: E
	): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof DataEntryMap,
		E extends keyof DataEntryMap[C] | (string & {}),
	>(
		collection: C,
		id: E
	): E extends keyof DataEntryMap[C]
		? Promise<DataEntryMap[C][E]>
		: Promise<CollectionEntry<C> | undefined>;

	/** Resolve an array of entry references from the same collection */
	export function getEntries<C extends keyof ContentEntryMap>(
		entries: {
			collection: C;
			slug: ValidContentEntrySlug<C>;
		}[]
	): Promise<CollectionEntry<C>[]>;
	export function getEntries<C extends keyof DataEntryMap>(
		entries: {
			collection: C;
			id: keyof DataEntryMap[C];
		}[]
	): Promise<CollectionEntry<C>[]>;

	export function reference<C extends keyof AnyEntryMap>(
		collection: C
	): import('astro/zod').ZodEffects<
		import('astro/zod').ZodString,
		C extends keyof ContentEntryMap
			? {
					collection: C;
					slug: ValidContentEntrySlug<C>;
				}
			: {
					collection: C;
					id: keyof DataEntryMap[C];
				}
	>;
	// Allow generic `string` to avoid excessive type errors in the config
	// if `dev` is not running to update as you edit.
	// Invalid collection names will be caught at build time.
	export function reference<C extends string>(
		collection: C
	): import('astro/zod').ZodEffects<import('astro/zod').ZodString, never>;

	type ReturnTypeOrOriginal<T> = T extends (...args: any[]) => infer R ? R : T;
	type InferEntrySchema<C extends keyof AnyEntryMap> = import('astro/zod').infer<
		ReturnTypeOrOriginal<Required<ContentConfig['collections'][C]>['schema']>
	>;

	type ContentEntryMap = {
		"changelog": {
"changelog.md": {
	id: "changelog.md";
  slug: "changelog";
  body: string;
  collection: "changelog";
  data: any
} & { render(): Render[".md"] };
};
"links": {
"links.md": {
	id: "links.md";
  slug: "links";
  body: string;
  collection: "links";
  data: any
} & { render(): Render[".md"] };
};
"now": {
"now.md": {
	id: "now.md";
  slug: "now";
  body: string;
  collection: "now";
  data: any
} & { render(): Render[".md"] };
};
"pins": {
"pins.md": {
	id: "pins.md";
  slug: "pins";
  body: string;
  collection: "pins";
  data: any
} & { render(): Render[".md"] };
};
"posts": {
"11-ways-uptime.md": {
	id: "11-ways-uptime.md";
  slug: "11-ways-uptime";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"allgpts.md": {
	id: "allgpts.md";
  slug: "allgpts";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"amphbunch.md": {
	id: "amphbunch.md";
  slug: "amphbunch";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"anew.md": {
	id: "anew.md";
  slug: "anew";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"applescript-gpt.md": {
	id: "applescript-gpt.md";
  slug: "applescript-gpt";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-3-3-picture-component.md": {
	id: "astro-3-3-picture-component.md";
  slug: "astro-3-3-picture-component";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-3-responsive-images.md": {
	id: "astro-3-responsive-images.md";
  slug: "astro-3-responsive-images";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-expressive-code.md": {
	id: "astro-expressive-code.md";
  slug: "astro-expressive-code";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-icon-v1.md": {
	id: "astro-icon-v1.md";
  slug: "astro-icon-v1";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-last-modified.md": {
	id: "astro-last-modified.md";
  slug: "astro-last-modified";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-markdown-image-story.md": {
	id: "astro-markdown-image-story.md";
  slug: "astro-markdown-image-story";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-pagefind.md": {
	id: "astro-pagefind.md";
  slug: "astro-pagefind";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-pagination.md": {
	id: "astro-pagination.md";
  slug: "astro-pagination";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-remark-eleventy-image.md": {
	id: "astro-remark-eleventy-image.md";
  slug: "astro-remark-eleventy-image";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-rss-compiledcontent.md": {
	id: "astro-rss-compiledcontent.md";
  slug: "astro-rss-compiledcontent";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-rss-update.md": {
	id: "astro-rss-update.md";
  slug: "astro-rss-update";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-sitemap-timestamps.md": {
	id: "astro-sitemap-timestamps.md";
  slug: "astro-sitemap-timestamps";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"astro-templates-json.md": {
	id: "astro-templates-json.md";
  slug: "astro-templates-json";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"audio-hijack-transcribe.md": {
	id: "audio-hijack-transcribe.md";
  slug: "audio-hijack-transcribe";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"autoimageprocess.md": {
	id: "autoimageprocess.md";
  slug: "autoimageprocess";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"bunch.md": {
	id: "bunch.md";
  slug: "bunch";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"chat-gpt-sherlock.md": {
	id: "chat-gpt-sherlock.md";
  slug: "chat-gpt-sherlock";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"cleanshotx-scrolling-screenshots.md": {
	id: "cleanshotx-scrolling-screenshots.md";
  slug: "cleanshotx-scrolling-screenshots";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"cleanshotx-text-recog.md": {
	id: "cleanshotx-text-recog.md";
  slug: "cleanshotx-text-recog";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"cool-site-spotlight.md": {
	id: "cool-site-spotlight.md";
  slug: "cool-site-spotlight";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"custom-links.md": {
	id: "custom-links.md";
  slug: "custom-links";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"default-apps-2023.md": {
	id: "default-apps-2023.md";
  slug: "default-apps-2023";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"default-browser.md": {
	id: "default-browser.md";
  slug: "default-browser";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"dimensions.md": {
	id: "dimensions.md";
  slug: "dimensions";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"draftsgpt.md": {
	id: "draftsgpt.md";
  slug: "draftsgpt";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"episode-image-script.md": {
	id: "episode-image-script.md";
  slug: "episode-image-script";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"fastmarks.md": {
	id: "fastmarks.md";
  slug: "fastmarks";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"for-myself.md": {
	id: "for-myself.md";
  slug: "for-myself";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"friends-with-transcripts.md": {
	id: "friends-with-transcripts.md";
  slug: "friends-with-transcripts";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"fwb2.md": {
	id: "fwb2.md";
  slug: "fwb2";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"fwbrews.md": {
	id: "fwbrews.md";
  slug: "fwbrews";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"git-commit-diffs.md": {
	id: "git-commit-diffs.md";
  slug: "gitcommitdiffs";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"git-pre-commit.md": {
	id: "git-pre-commit.md";
  slug: "git-pre-commit";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"gridtemplateareas.md": {
	id: "gridtemplateareas.md";
  slug: "gridtemplateareas";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"grin-and-bear-it.md": {
	id: "grin-and-bear-it.md";
  slug: "grin-and-bear-it";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"hypercritical-theme.md": {
	id: "hypercritical-theme.md";
  slug: "hypercritical-theme";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"image-rabbit-hole-1.md": {
	id: "image-rabbit-hole-1.md";
  slug: "image-rabbit-hole-1";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"image-rabbit-hole-2.md": {
	id: "image-rabbit-hole-2.md";
  slug: "image-rabbit-hole-2";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"image-rabbit-hole-3.md": {
	id: "image-rabbit-hole-3.md";
  slug: "image-rabbit-hole-3";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"image-text-recog.md": {
	id: "image-text-recog.md";
  slug: "image-text-recog";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"is-this-the-show.md": {
	id: "is-this-the-show.md";
  slug: "is-this-the-show";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"launchcontrol.md": {
	id: "launchcontrol.md";
  slug: "launchcontrol";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"link-posts.md": {
	id: "link-posts.md";
  slug: "link-posts";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"links-and-pins.md": {
	id: "links-and-pins.md";
  slug: "links-and-pins";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"mac-40.md": {
	id: "mac-40.md";
  slug: "mac-40";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"map-stuff.md": {
	id: "map-stuff.md";
  slug: "map-stuff";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"mastodon-webfinger.md": {
	id: "mastodon-webfinger.md";
  slug: "mastodon-webfinger";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"more-astro-image-markdown.md": {
	id: "more-astro-image-markdown.md";
  slug: "more-astro-image-markdown";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"now-page.md": {
	id: "now-page.md";
  slug: "now-page";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"one-more-thing.md": {
	id: "one-more-thing.md";
  slug: "one-more-thing";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"picture-sizes.md": {
	id: "picture-sizes.md";
  slug: "picture-sizes";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"podcasting-recording-practices.md": {
	id: "podcasting-recording-practices.md";
  slug: "podcasting-recording-practices";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"podcasting-recording-software.md": {
	id: "podcasting-recording-software.md";
  slug: "podcasting-recording-software";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"podcasting-setup-hardware.md": {
	id: "podcasting-setup-hardware.md";
  slug: "podcasting-setup-hardware";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"quicktune.md": {
	id: "quicktune.md";
  slug: "quicktune";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"raycast-ai-commands.md": {
	id: "raycast-ai-commands.md";
  slug: "raycast-ai-commands";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"raycast-ai-not-sherlocked.md": {
	id: "raycast-ai-not-sherlocked.md";
  slug: "raycast-ai-not-sherlocked";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"raycast-clipboard-history.md": {
	id: "raycast-clipboard-history.md";
  slug: "raycast-clipboard-history";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"raycast-sc-text-parsing.md": {
	id: "raycast-sc-text-parsing.md";
  slug: "raycast-sc-text-parsing";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"raycast.md": {
	id: "raycast.md";
  slug: "raycast";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"raycasting.md": {
	id: "raycasting.md";
  slug: "raycasting";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"redo-redoes-redid.md": {
	id: "redo-redoes-redid.md";
  slug: "redo-redoes-redid";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"remark-socials.md": {
	id: "remark-socials.md";
  slug: "remark-socials";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"rss-podcast.md": {
	id: "rss-podcast.md";
  slug: "rss-podcast";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"rss-pt1.md": {
	id: "rss-pt1.md";
  slug: "rss-pt1";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"rss-pt2.md": {
	id: "rss-pt2.md";
  slug: "rss-pt2";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"safari-bookmarks.md": {
	id: "safari-bookmarks.md";
  slug: "safari-bookmarks";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"sanitize-html.md": {
	id: "sanitize-html.md";
  slug: "sanitize-html";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"screenfloat.md": {
	id: "screenfloat.md";
  slug: "screenfloat";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"series-of-series.md": {
	id: "series-of-series.md";
  slug: "series-of-series";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"show-me-more.md": {
	id: "show-me-more.md";
  slug: "show-me-more";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"small-web.md": {
	id: "small-web.md";
  slug: "small-web";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"some-tags.md": {
	id: "some-tags.md";
  slug: "some-tags";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"theme-flicker.md": {
	id: "theme-flicker.md";
  slug: "theme-flicker";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"this-blog.md": {
	id: "this-blog.md";
  slug: "this-blog";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"title-case.md": {
	id: "title-case.md";
  slug: "title-case";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"warp-blocks.md": {
	id: "warp-blocks.md";
  slug: "warp-blocks";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
"whispering-transcripts.md": {
	id: "whispering-transcripts.md";
  slug: "whispering-transcripts";
  body: string;
  collection: "posts";
  data: any
} & { render(): Render[".md"] };
};
"uses": {
"uses.md": {
	id: "uses.md";
  slug: "uses";
  body: string;
  collection: "uses";
  data: any
} & { render(): Render[".md"] };
};

	};

	type DataEntryMap = {
		
	};

	type AnyEntryMap = ContentEntryMap & DataEntryMap;

	export type ContentConfig = never;
}
