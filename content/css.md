---
categories:
- Web-Development
title: css
---

# css

## How to exlude indirect children when working with `:not()`?

```css
main > *:not(.parallax) {
  @apply max-sm:px-2;
}
main > *:not(.parallax) * {
  @apply px-0; 
}

```
This example is done with TailwindCSS.

## How to expand div to the bottom fo the screen?
There is `h-screen` with makes the div as high as the screen allows. If you have another div above
for example a `<header>` you need to substract the height of `<header>` minus `h-screen`. This is how you do this:
```html
<header class="h-16"> <!-- h-16 => 4rem -->
</header>
<main class="min-h-[calc(100vh-4rem)]">
</main>
```
This example is done with TailwindCSS.

## Numbering for header-tag
On this website I found a trick how to use css for autonumbering: 

- https://2ality.com/2012/01/numbering-headingshtml.html

Completly without javascript (wow!).
```css
body {
  counter-reset: h2counter h3counter h4counter h5counter h6counter;
}

h2::before {
  counter-increment: h2counter;
  content: counter(h2counter) ". ";
  counter-set: h3counter 0;
}

h3::before {
  counter-increment: h3counter;
  content: counter(h2counter) "." counter(h3counter) ". ";
  counter-set: h4counter 0;
}

h4::before {
  counter-increment: h4counter;
  content: counter(h2counter) "." counter(h3counter) "." counter(h4counter) ". ";
  counter-set: h5counter 0;
}

h5::before {
  counter-increment: h5counter;
  content: counter(h2counter) "." counter(h3counter) "." counter(h4counter) "." counter(h5counter) ". ";
  counter-set: h6counter 0;
}

h6::before {
  counter-increment: h6counter;
  content: counter(h2counter) "." counter(h3counter) "." counter(h4counter) "." counter(h5counter) "." counter(h6counter) ". ";
}

```

