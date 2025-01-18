---
categories:
- Web-Development
title: css
---

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
