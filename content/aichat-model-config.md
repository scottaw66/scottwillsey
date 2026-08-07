+++
title = "aichat Config for OpenAI and Anthropic APIs"
description = "Configuring the aichat LLM CLI tool for OpenAI and Anthropic model use."
date = 2024-12-30T05:00:00-08:00
slug = "aichat-model-config"
[taxonomies]
tags = ["ai", "terminal"]
[extra]
display_title = "Aichat Config for OpenAI and Anthropic APIs"
display_date = "Monday, 30 Dec 2024"
rfc2822_date = "Mon, 30 Dec 2024 13:00:00 GMT"
+++

There is a fascinating LLM CLI tool called [aichat](https://github.com/sigoden/aichat) that lets you use all kinds of LLM models in the command line, including REPL mode, RAG mode (feeding it your documents and files of choice to use as a knowledgebase), and much more.

I was a little confused about how to configure it to give me a choice of OpenAI and Anthropic LLM models though. I kept breaking the config and generating error messages. Finally I stumbled across a post in the aichat repo’s closed issues that explained for OpenAI and Anthropic, you can configure their API and type information and skip configuring any model information. That way aichat will pull the list of available models from each API for you.

Here’s what my config looks like now:

```bash title="~/Library/Application Support/aichat/config.yaml"

model: claude:claude-3-5-sonnet-latest
stream: true
save: true
wrap: 85
wrap_code: false
clients:
- type: openai
  api_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

- type: claude
  api_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx         
```

You can see I default to the Claude 3.5 Sonnet (latest) model. The nomenclature for the value of specified model is `type:model-name`. Then I have a clients section which lists two types of models: OpenAI and Claude (Anthropic).

Here’s the default Claude 3.5 Sonnet (which is notoriously shy about answering questions about model information):

```bash
scott@Midnight:~ ➜ aichat "what model are you using?"
I'm Claude, an AI assistant created by Anthropic. I aim to be direct and honest in my
communications, including about what I am.
```

But I could also specify a model manually, or set it in an environment variable:

```bash
scott@Midnight:~ ➜ aichat -m openai:gpt-4o "What LLM model are you using?"
I am based on OpenAI's GPT-4 model.
```

And in aichat REPL mode, you can get a list of models to choose from with the `.model ⇥` command (that’s .model followed by a space and a tab).

```bash {5}
scott@Midnight:~ ➜ aichat
Welcome to aichat 0.26.0
Type ".help" for additional help.
> | .model 
openai:gpt-4o                        128000 /    16384  |     2.5 /     10    👁 ⚒ 
openai:gpt-4o-2024-11-20             128000 /    16384  |     2.5 /     10    👁 ⚒ 
openai:gpt-4o-2024-08-06             128000 /    16384  |     2.5 /     10    👁 ⚒ 
openai:chatgpt-4o-latest             128000 /    16384  |       5 /     15    👁 ⚒ 
openai:gpt-4o-mini                   128000 /    16384  |    0.15 /    0.6    👁 ⚒ 
openai:gpt-4-turbo                   128000 /     4096  |      10 /     30    👁 ⚒ 
openai:o1-preview                    128000 /    32768  |      15 /     60        
openai:o1-mini                       128000 /    65536  |       3 /     12        
openai:o1                            128000 /        -  |      15 /     60    👁 ⚒ 
openai:gpt-3.5-turbo                  16385 /     4096  |     0.5 /    1.5      ⚒ 
claude:claude-3-5-sonnet-latest      200000 /     8192  |       3 /     15    👁 ⚒ 
claude:claude-3-5-sonnet-20241022    200000 /     8192  |       3 /     15    👁 ⚒ 
claude:claude-3-5-haiku-latest       200000 /     8192  |     0.8 /      4    👁 ⚒ 
claude:claude-3-5-haiku-20241022     200000 /     8192  |     0.8 /      4    👁 ⚒ 
claude:claude-3-opus-20240229        200000 /     4096  |      15 /     75    👁 ⚒ 
claude:claude-3-sonnet-20240229      200000 /     4096  |       3 /     15    👁 ⚒ 
claude:claude-3-haiku-20240307       200000 /     4096  |    0.25 /   1.25    👁 ⚒ 
```

Arrow up and down to select the model you want and then hit return. This basically does the same as you typing `.model type:model-name`:

```bash
scott@Midnight:~ ➜ aichat
Welcome to aichat 0.26.0
Type ".help" for additional help.
> .model openai:gpt-4o

> what LLM model are you?
I am based on OpenAI's GPT-4.
```

There’s a lot that aichat can do that I haven’t even poked at yet. Honestly, I don’t have time and probably use cases to dig into it much more in the very near term, but it is definitely a very comprehensive CLI tool for LLM use.
