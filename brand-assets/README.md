# Brand Assets

This directory is now the local-first source package for the brand system.

Use it in two ways:

1. Treat the files here as the working source of truth while Figma access is limited.
2. Import the SVG templates into Figma later to rebuild the same system visually.

## Structure

- `system/`
  - brand rules, tokens, and prompt guidance
- `logo/`
  - starter SVG logo assets
- `icons/`
  - starter SVG icon set
- `slide-assets/`
  - SVG templates for lecture slides
- `social/`
  - SVG templates for X, LinkedIn, and YouTube
- `web/`
  - SVG templates for website hero and supporting modules

## Core Direction

- Brand type: personal master brand with course sub-brand
- Tone: editorial tech
- Primary use case: slides first
- Accent color: electric blue only
- Default surfaces: light for teaching, dark for covers and banners

## Fonts

- Display: `Space Grotesk`
- Body/UI: `IBM Plex Sans`
- Code: `IBM Plex Mono`

If these fonts are unavailable in your current tool, use:

- Display fallback: `Inter`
- Body fallback: `Inter`
- Code fallback: `Roboto Mono`

## Import Workflow

1. Review the rules in [brand-system.md](/Users/lukaslechner/PythonProjects/ai-engineering-foundations-labs/brand-assets/system/brand-system.md).
2. Import the needed SVG files into Figma or Figma Slides.
3. Rebuild them as components or slide masters if you want a fully native Figma system.
4. Keep generated images consistent using [generated-image-prompts.md](/Users/lukaslechner/PythonProjects/ai-engineering-foundations-labs/brand-assets/system/generated-image-prompts.md).

## Recommended Export Targets

- `logo/`: wordmark, dark wordmark, course lockup, monogram
- `icons/`: approved SVG icons
- `slide-assets/`: cover, divider, content, code, diagram, quote
- `social/`: X banner, LinkedIn banner, YouTube thumbnail
- `web/`: desktop hero, mobile hero, feature card, section header
