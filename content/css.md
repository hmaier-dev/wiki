---
categories:
- Web-Development
title: css
---

# Classic CSS

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

# TailwindCSS

## How to expand div to the bottom fo the screen?
There is `h-screen` with makes the div as high as the screen allows. If you have another div above
for example a `<header>` you need to substract the height of `<header>` minus `h-screen`. This is how you do this:
```html
<header class="h-16"> <!-- h-16 => 4rem -->
</header>
<main class="min-h-[calc(100vh-4rem)]">
</main>
```
