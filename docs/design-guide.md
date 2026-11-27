# Trading Simulator: UX and UI Design Guide v1

Nov 27, 2026 · Prafull Kotecha

This guide turns the Product Spec v1 into a buildable design system and screen set for the Flutter apps and the PWA. Anything the spec did not already decide is marked **Proposed**.

## Principles

Every screen should feel calm, precise and honest, the way a good flight simulator feels: real controls, safe consequences. Seven principles decide every trade-off, in this order when they conflict.

1. **Honest by default.** Simulated money and synthetic prices are never hidden. Every price carries a "Simulated price" label, every option price a "Modeled" badge, and nothing looks like a real brokerage offer.
2. **Show, then tell.** The picture carries the idea and words point at it. Each lesson has one diagram the learner can drag, and text refers to what is on screen ("the dashed line is your strike").
3. **One idea per screen.** A screen has one job and one primary action. Secondary detail lives one tap away in a sheet, never in a crowded panel.
4. **Risk is always visible.** Before any order, the learner sees what it costs, the most it can lose and, for options, the breakeven. Max loss is never behind a tap.
5. **Same marks everywhere.** Blue is gain, orange is loss, a dashed line is a strike, a ring is a breakeven, and every value is also printed as a signed number. A learner who learns a mark in L1 can read it in L4.
6. **Calm, not casino.** No confetti on profits, no flashing tickers, no countdown pressure, no slot-machine sounds. Celebration is reserved for learning: passing a quiz, unlocking a level, finishing a challenge within its risk rule.
7. **Fast and quiet.** Screens open in under a second, charts run at the display's refresh rate, and the app speaks only when it has something useful to say.

Two learners test every screen: Maya, 15, on her phone for 5 to 15 minutes in the evening, and Dev, 34, on a phone or laptop at lunch. If a screen bores Maya or confuses Dev, it is not done.

## Color

The palette is a custom Material 3 color scheme with two money colors that never change meaning: blue for gain and orange for loss. Dark is the default theme, as the spec decided; light is a full equal, and a "Match system" option in Settings is **Proposed**. Every text pair below passes WCAG 2.2 AA (4.5:1), and every input border passes the 3:1 non-text rule.

*Figure not included in this Markdown copy: core color tokens · dark and light.*

| Role (Flutter `ColorScheme` or extension) | Dark (default) | Light | Used for |
| --- | --- | --- | --- |
| `surface` | #0F1217 | #FAFBFC | App background |
| `surfaceContainer` | #171B22 | #FFFFFF | Cards, lesson body |
| `surfaceContainerHigh` | #1F242D | #EEF1F5 | Sheets, trade ticket, chain rows |
| `onSurface` | #E9ECF1 (15.8:1) | #12161C (17.5:1) | Primary text, figures |
| `onSurfaceVariant` | #A9B2C0 (8.8:1) | #4A5361 (7.5:1) | Secondary text, axes, strike lines |
| `outline` | #6B7586 (3.4:1 on high) | #7A8391 (3.4:1 on high) | Input and control borders |
| `outlineVariant` | #2C323C | #D9DEE5 | Dividers, chart grid (decorative only) |
| `primary` | #B3A6FF (8.8:1) | #5B43D6 (6.3:1) | Brand: primary buttons, selected nav, links, focus ring |
| `onPrimary` | #1E1060 (7.6:1) | #FFFFFF (6.5:1) | Text on primary |
| `primaryContainer` / `onPrimaryContainer` | #2E2470 / #E6E0FF | #E6E0FF / #1E1060 | Selected chips, level badges, progress |
| `gain` (extension) | #5DB2F2 (8.1:1) | #0B66B8 (5.6:1) | Positive P&L, payoff above zero, up moves |
| `gainContainer` (extension) | #0E2A40 | #DCEEFC | Profit zone fill under a payoff line |
| `loss` (extension) | #FF9F45 (9.2:1) | #B24E00 (5.1:1) | Negative P&L, payoff below zero, down moves |
| `lossContainer` (extension) | #3D2410 | #FFE8D4 | Loss zone fill under a payoff line |
| `error` / `onError` | #FFB4AB / #690005 | #BA1A1A / #FFFFFF | Form and system errors only, never P&L |
| `scrim` | #000000 at 60% | #000000 at 40% | Behind sheets and dialogs |

Contrast ratios are against `surface`; all text pairs also pass on `surfaceContainerHigh`.

Rules for color:

- **Money colors mean money.** Blue and orange appear only for gain, loss and the direction of a price move. They are never used for buttons, levels, quiz feedback or decoration.
- **Buy and Sell are not colored.** Buy and Sell use the same brand button styles and differ by label and icon, so selling never reads as "danger" and buying never reads as "profit". (**Proposed**; brokers often color them green and red, which teaches the wrong instinct.)
- **Brand violet stays out of data.** `primary` never appears inside a chart's plot area, because some color-blind learners see violet close to the gain blue.
- **Color is never alone.** Every gain or loss also shows a sign (+ or −), and charts add a pattern or label where color carries meaning (see Charts).
- **Errors are red, losses are orange.** A loss is a normal outcome, not a mistake, so it never uses the error color.
- **No company colors.** Tickers are plain text with no logos or brand colors, as the spec requires.
- **Level marks reuse the brand.** Levels are told apart by an icon and numeral, not new hues: L1 Seed, L2 Sprout, L3 Stalk, L4 Harvest, following the farm analogy (**Proposed**).
- In Flutter, gain and loss live in a `ThemeExtension` (`MarketColors`) so widgets read `Theme.of(context).extension<MarketColors>()` and never hard-code a hex value.

## Type, spacing, shape and elevation

Type is generous and numbers never jump: two open-license families, bundled with the app, on the Material 3 type scale with three extra roles for figures (**Proposed**).

- **Space Grotesk** for display and headline roles: friendly, a little technical, distinct from banking apps.
- **Inter** for everything else, with tabular figures (`FontFeature.tabularFigures()`) on every price, quantity and P&L so digits line up and do not shift as they tick.
- Fonts ship as app assets, never fetched from a font CDN at runtime, so the PWA works offline and makes no third-party request.

| Role | Family, weight | Size / line height | Where |
| --- | --- | --- | --- |
| Display S | Space Grotesk 600 | 36 / 44 | Level unlock, challenge result |
| Headline M | Space Grotesk 600 | 28 / 36 | Screen titles on tablet and web |
| Headline S | Space Grotesk 600 | 24 / 32 | Screen titles on phone, lesson title |
| Title L | Inter 600 | 22 / 28 | Card titles, sheet titles |
| Title M | Inter 600 | 16 / 24 | List item titles, section labels |
| Body L (lesson) | Inter 400 | 18 / 28 | Lesson reading text (**Proposed**: larger than Material's 16 for comfort) |
| Body L | Inter 400 | 16 / 24 | Default body |
| Body M | Inter 400 | 14 / 20 | Secondary text, captions under charts |
| Label L | Inter 600 | 14 / 20 | Buttons, tabs, chips |
| Label M | Inter 500 | 12 / 16 | Badges, "Simulated price" and "Modeled" labels |
| Figure XL | Inter 600, tabular | 40 / 48 | Account value on Portfolio |
| Figure L | Inter 600, tabular | 28 / 36 | Price on ticker and replay header |
| Figure M | Inter 500, tabular | 16 / 24 | Prices in lists, chains, tickets |

Type rules: nothing below 12 sp; sizes are in sp so they follow the system text-size setting up to 200%; tickers are written in Inter 600 caps with no extra letter-spacing; a minus sign is the true minus (−), never a hyphen.

**Spacing** uses a 4-point grid with eight steps: 4, 8, 12, 16, 24, 32, 48 and 64. Page margins are 16 on phones and 24 on tablets and desktops; cards pad 16 inside; list rows are at least 56 tall; and every touch target is at least 48 by 48 dp, above the WCAG 2.2 minimum of 24 by 24.

**Shape** follows Material 3 corner tokens: 4 for chips and badges, 8 for text fields, 12 for cards, 16 for the trade ticket and dialogs, 28 for bottom sheets' top corners, and full rounding for buttons, the scrubber thumb and level icons.

**Elevation** is tonal, not shadowed. Depth comes from the surface container steps in Color; a shadow appears only on the floating timeline scrubber and on sheets while they are dragged, so the flat, calm look holds in both themes.

## Motion

Motion explains cause and effect and never decorates money. A payoff line that bends as days pass is good motion; a confetti burst on a winning trade is not.

| Token | Duration | Easing (Material 3) | Use |
| --- | --- | --- | --- |
| `motion.tick` | 120 ms | standard (0.2, 0, 0, 1) | A price or P&L value changing; digits cross-fade, never slot-roll |
| `motion.short` | 200 ms | standard | Chips, toggles, state layers, tooltips |
| `motion.medium` | 300 ms | emphasized decelerate (0.05, 0.7, 0.1, 1) | Sheets opening, cards expanding, payoff line morphing after a drag ends |
| `motion.long` | 450 ms | emphasized (0.2, 0, 0, 1) | Screen transitions (shared axis on phone, fade-through on web) |
| `motion.exit` | 150 ms | emphasized accelerate (0.3, 0, 0.8, 0.15) | Sheets and dialogs closing |
| `motion.celebrate` | up to 1,200 ms | emphasized | Level unlock and challenge pass only; tap to skip |

Motion rules:

- **Direct manipulation is instant.** While a finger drags price, strike or days left on a diagram, the chart follows the finger every frame with no easing; easing applies only after release.
- **Replays move, the interface does not.** During playback only the chart, the clock and the figures change; panels never slide or bounce.
- **Pauses are visible.** When the clock pauses on a news beat or a fill, the play button morphs to a pause state and the beat card rises in 300 ms, so the learner knows why time stopped.
- **Reduce motion.** When the system's reduce-motion setting is on (`MediaQuery.disableAnimations` on mobile, `prefers-reduced-motion` on the web), transitions become 100 ms fades, celebrations become a static badge, and replays default to the slowest speed. Playback itself stays, because it is the content, and it can always be paused (WCAG 2.2.2).
- **No flashing.** Nothing flashes more than three times a second (WCAG 2.3.1); price changes never flash a background color.
- **Haptics are rare** (**Proposed**): a light tick when a drag handle snaps to a strike, a medium impact when an order fills, and nothing for gains or losses.

## Components

The app uses Material 3 components re-skinned by the theme wherever one fits, and builds a small set of custom components for the money and learning moments. Custom components are `CustomPainter` widgets, as the spec's architecture requires, and each one ships with golden tests in both themes.

Every interactive component has the same six states: enabled, hovered (web and tablet with a pointer), focused, pressed, dragged where it applies, and disabled. State layers follow Material 3 opacities (hover 8%, focus and press 10%, drag 16%). The focus ring is a 2 dp `primary` outline offset 2 dp from the component, always visible and never clipped.

**Material 3 components, themed**

| Component | Variant and rule |
| --- | --- |
| Navigation bar / rail / drawer | Bar on phones, rail on tablets, drawer on wide web; 5 destinations (see Navigation) |
| Top app bar | Small, centered title; trailing profile icon opens You and Settings |
| Buttons | Filled for the one primary action per screen; tonal for secondary; outlined for "Review" and "Cancel order"; text buttons for links |
| Segmented button | Buy / Sell, Call / Put, order type, replay speed (1 day per 10, 30 or 60 seconds) |
| Chips | Filter chips for lesson and scenario lists; assist chips for "Try it"; label chips for status (below) |
| Cards | Filled cards on `surfaceContainer`; no outlined cards except selected states |
| Bottom sheet | Trade ticket, term definitions, greeks explainers, beat cards; drag handle always shown |
| Dialog | Only to confirm leaving a replay mid-play and to confirm an account reset; never for orders (orders use a review step in the sheet) |
| Snackbar | Order filled, order cancelled, saved offline; never for errors that need action |
| Progress | Linear for lesson and level progress; circular only for loading over 400 ms |
| Slider | Replay speed, diagram drags where a handle is not on the chart |
| Text field | Filled style; numeric keypad for quantity and price; errors under the field in `error` with an icon |
| Tooltip / rich tooltip | Pointer hover on web only; touch uses a sheet instead |
| Badge | Unread debrief dot on Replays; never a count that nags |

**Status labels.** Three small label chips appear wherever their facts apply, in Label M on `surfaceContainerHigh` with `onSurfaceVariant` text and a leading icon, and they are never hidden on small screens:

- "Simulated price" (clock-with-wave icon) on every price, chart and ticket.
- "Modeled" (function icon) on every option price, chain and greek.
- "Modeled on March 2020" (or the event) on every scenario card and replay header.

**Custom components**

| Component | What it does | Key rules |
| --- | --- | --- |
| Replay timeline scrubber (signature) | Horizontal timeline under the replay chart; thumb drag rewinds to review; the live head is marked | Orders can be placed only at the live head; rewinding greys the trade button with "Return to live to trade"; 48 dp thumb; keyboard ← → step one bar, Shift for ten |
| Payoff diagram (signature) | Profit at expiry and today for a position; drag price, strike or days left | Zero line always drawn; profit zone filled `gainContainer`, loss zone `lossContainer`; strike dashed; breakeven a ring with its price; max gain and max loss labeled in dollars |
| Price chart | Line by default, candles from lesson 1.3 on; volume bars optional | See Charts; "Simulated price" label in the chart's top-left |
| Trade ticket | Order entry in a sheet (phone) or side panel (tablet, web) | Shows cost, cash after, max loss and breakeven before the Review button; quantity stepper plus keypad |
| Option chain | Strikes in rows, calls left, puts right, one expiry at a time | Stock price drawn as a line between rows; in-the-money cells tinted; tap a price to open the ticket prefilled |
| Greeks card | Delta, gamma, theta and vega as dollars per contract | Each greek has a one-line plain meaning and a farm line in its info sheet |
| Position card | Ticker, quantity, cost, value, P&L in dollars and percent | P&L colored and signed; options show days left and a mini payoff sparkline |
| Lesson diagram frame | Hosts each lesson's one interactive diagram | Drag handles 48 dp with a visible grip; a "Reset" text button; live numbers printed beside the chart |
| Term chip | A bold new term inside lesson text | Tap opens a sheet with the one-line definition and its farm line; never a hover-only popover |
| Quiz answer tile | One answer option, full width | Selected, correct and wrong states use icon plus text ("Correct", "Not quite"), not color alone |
| Debrief card | One debrief section: went well, mistakes, study next | Mistakes link to the moment on the timeline; "Study next" opens the lesson |
| Level badge | Seed, Sprout, Stalk, Harvest icon with level numeral | Locked badges show a lock and what unlocks them |
| Leaderboard row | Rank, generated nickname, score, level badge | No photo, no location, no free text; the learner's own row is pinned and highlighted |
| Disclaimer banner | The spec's educational disclaimer | Persistent footer on web screens; on mobile at signup, in Settings and on every debrief |
| Break prompt | Gentle prompt after 45 minutes of continuous play for under-18s | A sheet, not a blocker: "Take a break" and "Keep going" |

Empty, loading and error states are part of every component: skeletons in `surfaceContainerHigh` for content under 1 second, a short line of help text plus one action for empty states, and an inline retry for errors. Offline states say what still works ("Downloaded replays still play").

## Navigation

Five top-level destinations follow the core loop, and the trade ticket is one shared component reached from Replays, Live and Portfolio (**Proposed**: the spec set the loop but not the tabs).

*Figure not included in this Markdown copy: app map · 5 tabs and the shared trade ticket.*

Learn is home. A lesson's "Try it" jumps straight into a seeded replay, and the replay's debrief links back to the next lesson, so the loop never needs the tab bar.

- **Learn:** level path, lessons, quizzes, gate challenges, level unlocks.
- **Replays:** scenario library by level and event, downloaded packs, past results and debriefs.
- **Live:** the simulated live market of about 100 real tickers, each ticker's chart and, from L2, its option chain.
- **Challenges:** this week's challenge, leaderboards and friends by invite code.
- **Portfolio:** the live paper account: value, positions, orders and the weekly reset.
- **You** (top bar, not a tab): profile and nickname, settings (theme, streaks, notifications, shortcuts, data export and delete), help and glossary, and the disclaimer.

Rules: the tab bar hides during a replay and inside the ticket to give the chart room; back always returns to where the learner came from; and a deep link (a lesson URL on the web, a notification on mobile) opens its screen with the tab bar restored underneath.

## Key screens and flows

Ten screens carry the whole product. Each is described top to bottom on a compact phone, with its one primary action; wider layouts follow Responsive. Wireframes show the busiest screens.

*Figure not included in this Markdown copy: wireframes · home, replay, trade ticket, payoff (dark theme marks).*

### Onboarding

The goal is a first practice trade within 3 minutes of opening the app, with only the data the spec allows.

1. **Welcome:** the app name, one line ("Learn to invest by replaying real market moments with simulated money"), and "Get started". The web version is the landing page, with the 13+ gate and the disclaimer.
2. **Birthdate:** a neutral date picker with no default year and no hint of the right answer. Under 13 sees a kind "Come back when you're 13" screen and nothing is stored.
3. **Sign in:** Apple, Google or email link, in that order on iOS and Google first on Android and web (**Proposed**). No password.
4. **Nickname:** a generated nickname ("Calm Otter 482") with a reroll button; it can never be typed.
5. **Disclaimer:** the full educational disclaimer with one "I understand" button. It is an acknowledgment, not a certification checkbox.
6. **First lesson:** onboarding ends inside lesson 1.1, not on a dashboard, and that lesson's "Try it" is the first practice trade.

No notification prompt, streak setup or tour appears during onboarding.

### Home (Learn)

Home answers "what do I do next?" in one glance.

- **Next up card** (primary): the next lesson or the replay its "Try it" opens, with time ("4 min") and one filled button, "Continue".
- **Level path:** the four levels as a vertical path with Seed, Sprout, Stalk and Harvest icons; the current level expanded to show its lessons as rows with check marks; locked levels show what unlocks them.
- **This week's challenge** card, when one is open, with days left and the learner's best practice score.
- **Latest debrief** card if one is unread.

There is no market news feed, no trending list and no portfolio total on Home, which keeps learning first.

### Lesson

One lesson is one scrolling screen in four parts that match the lesson plan: read with the diagram, check, try it, and a link to the debrief afterwards.

- Header: lesson number and title, a 4-step progress line, close button.
- **Farm line** in italics, one sentence.
- **Goal** in Title M.
- **Diagram frame**, sticky at the top while the text scrolls under it on compact screens; handles, steppers and live numbers as in Components.
- **Text** in Body L (lesson), with bold term chips.
- **Check:** two or three quiz tiles answered on the diagram where possible ("Drag the price to where this call breaks even").
- **Try it:** one filled button that opens the seeded replay.

### Replay

The replay screen is the heart of the app; it has to work one-handed on a phone.

- **Header:** scenario name, "Modeled on March 2020" label, the market date and the simulated clock.
- **Price chart** of the selected ticker with fills, news flags and order lines; ticker switcher as a horizontal chip row of the scenario's universe.
- **Account strip:** cash, positions value and P&L since start, signed and colored.
- **Timeline scrubber** above the bottom controls, with play/pause and speed.
- **Primary action:** a full-width "Trade" button that opens the ticket; it becomes "Return to live to trade" while rewound.
- **News beats** pause the clock and rise as a card with the headline and "Resume".
- **End:** a result card with return, max drawdown, objective pass or fail, and "See debrief". Study mode is a secondary button.

Leaving mid-replay asks once ("Leave this replay? Progress is saved").

### Trade ticket

The ticket makes the cost and risk of every order visible before it is placed.

1. **Build:** Buy/Sell segmented control, ticker and simulated price, quantity stepper, order type (market, limit, stop, stop-limit), limit or stop price, day or good-till-cancelled.
2. **Risk panel**, always visible: estimated cost, cash after, max loss, and for options the breakeven and a mini payoff diagram.
3. **Review:** a summary in plain words ("Buy 10 SPY at market, about $4,124.50"), then "Place order". The ticket never places an order in one tap.

Collateral rules from the spec show as plain blocks, not errors after the fact: "Selling this put sets aside $9,500 of cash." Orders the learner's level does not allow are not offered; the locked type shows what unlocks it.

### Option chain and payoff diagram

- **Chain:** expiry chips across the top (weeklies and monthlies, with days left), calls left and puts right, strikes down the middle, the stock price drawn as a line between strikes, in-the-money cells tinted, "Modeled" label. On compact phones the chain shows one side at a time with a Calls/Puts switch (**Proposed**), because both sides plus strikes do not fit at 360 dp.
- **Tapping a price** opens the ticket with that contract; L4 spreads add a second leg by tapping a second strike, and the payoff diagram updates as legs are added.
- **Payoff diagram** sits at the top of the options ticket and on every option position: drag price and days left; max gain, max loss and breakeven printed; greeks card below it.

### Debrief

The debrief turns the result into one thing to learn next.

- Header: scenario, result in one line, and the disclaimer link.
- **Takeaway** first, one sentence in Title L.
- **Went well:** up to three items. **Mistakes:** up to three, each with a "See on timeline" link that opens the replay at that moment.
- **Study next:** one lesson card with "Open lesson".
- When the daily cap is used, the template debrief uses the same layout with the computed facts and no AI text, and says so in one line.

### Level unlock

Unlocking a level is the one big celebration. The flow is: quiz (10 to 15 questions, one per screen, 80% to pass), then the gate replay challenge with its risk rule shown before start, then the unlock screen.

- The new level icon grows from the previous one (Sprout from Seed) in up to 1,200 ms, skippable, static under reduce motion.
- One line on what is now allowed ("You can now sell covered calls and cash-secured puts") and "Start Level 2".
- A failed quiz shows the score, the two lessons to review and "Retake" after review; nothing is lost, and levels never re-lock.

### Challenges

- **This week:** the scenario, its goal and risk rule, days left, "Practice" (unlimited, unscored) and "Play scored run" (once).
- **Leaderboards:** Global, My level and Friends tabs; rows as in Components; the learner's row pinned; "Hide me from global" switch for under-18s on this screen.
- **Friends:** show my invite code and enter a code; remove a friend from a row's menu. No search, no contact upload.
- **Past challenges:** results and badges.

### Portfolio

Portfolio shows the live paper account; replay accounts live inside their replays.

- **Account value** in Figure XL, "Simulated price" label, P&L today and since start, both signed.
- **Value chart** with a range switch (1D, 1W, 1M, all) and the max drawdown band.
- **Positions** list of position cards, options grouped by strategy (a spread shows as one card with two legs).
- **Orders:** open and filled, with cancel on open orders.
- **Weekly reset** sits in the overflow menu with a confirm dialog, as the spec allows one reset a week.
- During market closed hours, a quiet banner says when the simulated market opens.

## Charts and data visualization

Charts are the main teaching surface, so they follow one grammar across lessons, replays, live mode and debriefs. A learner who reads one chart can read them all.

**The fixed marks**

| Mark | Meaning | Drawn as |
| --- | --- | --- |
| Blue | Gain, profit zone, up move | `gain`; fills use `gainContainer` |
| Orange | Loss, loss zone, down move | `loss`; fills use `lossContainer` |
| Dashed line | A strike or an order level (limit, stop) | 1.5 dp dash 6 / gap 4 in `onSurfaceVariant`, labeled at its right end ("Strike $105", "Stop $96") |
| Ring | A breakeven | 10 dp open circle in `onSurface` with its price beside it |
| Solid dot | A fill (where an order executed) | 8 dp dot in `onSurface` with a B or S glyph, never blue or orange, because buying is not a gain |
| Thin line | Value today (before expiry) | 1.5 dp, `onSurfaceVariant` |
| Thick line | Value at expiry, or the main series | 2.5 dp, `onSurface`, colored by zone only in payoff diagrams |
| Shaded band | A drawdown, a range, or the stock price's likely spread | `outlineVariant` at 40%, labeled with its size ("−22.4% drawdown") |

**Rules every chart follows**

1. **A title that says the finding**, not the topic: "Your stop filled $3.10 below where you set it", not "Stop order fill".
2. **Labeled axes with units.** Price axes in dollars, time axes in trading days or market time, profit axes in dollars per position (× 100 shares for options is already applied).
3. **The zero line is always drawn** on profit and P&L charts, in `onSurfaceVariant`, so above-or-below reads at a glance.
4. **Values are printed, not only plotted.** Every chart shows its key numbers as signed text beside it (current price, P&L, max loss, max gain, breakeven), so the chart works for screen readers and color-blind learners.
5. **Direct labels beat legends.** Series are labeled at their line ends; a legend appears only when lines would collide.
6. **No 3D, no gradients, no dual axes**, and no pie charts; parts of a whole (an ETF's holdings) use a treemap or stacked bar.
7. **Grid lines are quiet**: horizontal only, `outlineVariant`, at most five.
8. **Price lines are lines.** Candles appear only once lesson 1.3 has taught them; learners can switch between line and candle on any price chart after that.
9. **Scales are honest.** Price axes may start above zero but say so with a broken-axis mark; percent and P&L axes always include zero.
10. **Every chart is touchable.** Touch and hold shows a crosshair with the date, price and P&L at that point; on the web, hover does the same and arrow keys move the crosshair.

**Payoff diagram specifics.** The x-axis is the stock price at expiry, centered on the current price and spanning about ±30% (wider for L4 spreads if a strike falls outside). The y-axis is profit in dollars. The thick line is the position at expiry, the thin line is its value today, and dragging "days left" moves the thin line toward the thick one, which is the spec's "motion that explains". Max gain and max loss are printed as flat labels on their plateaus, or "Unlimited" with an arrow where a line keeps rising. The current price is a vertical line labeled "Now $101.20".

**Replay chart specifics.** The live head sits at 85% of the chart's width so there is room ahead; news beats are flags on the time axis that open their card on tap; the learner's fills are dots on the price line; and in study mode, the future part of the path, revealed after the replay ends, is drawn in `onSurfaceVariant` so the learner can tell what they saw live from what came after.

**Number formatting.** Prices always to two decimals; account totals of $10,000 or more round to whole dollars in summaries, with full cents in tickets; percents to one decimal; signs always shown on changes (+$12.40, −0.8%); thousands separators by locale; and option prices per share in chains with the ×100 contract cost shown in the ticket.

## Content and microcopy voice

The app sounds like a sharp, patient coach: plain, specific and warm, never hype. It writes for a smart 13-year-old, which also suits a busy adult, and it follows the lesson rule "as simply as possible with easy to follow visuals".

**Voice in four traits**

| Trait | Means | Write | Don't write |
| --- | --- | --- | --- |
| Plain | Everyday words; a term is bolded and defined the first time | "You buy at the ask, the higher price." | "Execution occurs at the prevailing offer." |
| Specific | Real numbers and the learner's own trade | "Your stop filled at $92.90, $3.10 below $96." | "Slippage occurred." |
| Calm | Losses are lessons, not drama | "Down 8% on this trade. The debrief shows why." | "Ouch! You got crushed!" |
| Honest | Simulated is always said, never implied away | "Simulated price" / "Modeled on March 2020" | "Live AAPL price" / "Real market data" |

**Rules**

- **Sentence case** everywhere, including buttons and titles.
- **Buttons say what happens:** "Review order", "Place order", "Start replay", "Retake quiz". Never "OK", "Submit" or "Go".
- **Second person, active voice**: "You own 10 shares", not "10 shares are owned".
- **Short:** button labels up to 3 words, lesson sentences under 20 words, one idea per sentence.
- **The farm analogy is one line per lesson**, at the top, in italics, then the text switches to real tickers and dollars. The glossary gives each term its "think of it like". No other metaphors anywhere, including microcopy.
- **No advice, no signals, no hype.** Never "you should buy", "top picks", "hot stock", "to the moon", "get rich" or rocket and money-bag emoji. The debrief schema and safety filter enforce this for AI text; the same list applies to human-written copy.
- **Every disclaimer is short where it appears** and full where the spec requires it: the label chips on prices, the full disclaimer at signup, in Settings, on every debrief and in the web footer.
- **Numbers carry signs and units** as in Charts; tickers appear as plain text with no logos.
- **Errors say what happened and what to do**: "Not enough cash. This order needs $2,410 and you have $1,980. Lower the quantity or sell something first."
- **Empty states teach**: "No positions yet. Your first lesson ends with a practice trade."

**Key strings** (**Proposed** wording, for the copy deck)

| Moment | Copy |
| --- | --- |
| Order review header | "Check your order" |
| Max loss line | "Most you can lose: $360" |
| Breakeven line | "Breaks even at $104.00 at expiry" |
| Rewound timeline | "You're looking back. Return to live to trade." |
| News beat pause | "Paused for news" |
| Debrief cap reached | "Today's coach debrief is used. You'll get a summary now and a full debrief tomorrow." |
| Quiz fail | "Not yet: 9 of 15. Review two short lessons, then try again." |
| Level unlock | "Level 2 unlocked: covered calls and cash-secured puts" |
| Break prompt | "You've been at it for 45 minutes. Want a break?" |
| No-affiliation note | "Prices are simulated. Apple Inc. has no connection to this app." |

Teens and adults get the same words. The AI debrief adjusts tone only through the spec's "teen" or "adult" bucket, a little warmer for teens, and never changes the facts.

## Accessibility and teen safety

The target is WCAG 2.2 AA on iOS, Android and the web, one step above the spec's WCAG 2.1 AA; the spec's Design system section should be read as 2.2 AA from here on. Accessibility is tested on every release, not audited at the end.

**What 2.2 AA means for this app**

| Criterion | How the app meets it |
| --- | --- |
| 1.4.3 / 1.4.11 Contrast | Token pairs in Color pass 4.5:1 for text and 3:1 for borders, chart lines and focus rings in both themes |
| 1.4.1 Use of color | Gain and loss always have a sign and an arrow; quiz states have icons and words; chart zones are labeled |
| 1.4.4 / 1.4.10 Resize and reflow | Text scales to 200% with no clipping; at 320 CSS px wide the web app reflows to one column with no sideways scrolling, except inside charts, which pan |
| 2.1.1 Keyboard | Every action on the web works by keyboard, including diagram drags (arrow keys move the focused handle by one step, Shift by ten) and the scrubber |
| 2.2.2 Pause, stop, hide | Replays always have a visible pause; the live market's moving prices can be frozen with "Pause updates" |
| 2.4.7 / 2.4.11 Focus visible, not obscured | The 2 dp focus ring is never covered by the sticky trade button, nav bar or a sheet; focused items scroll into view above them |
| 2.5.7 Dragging movements | Every drag has a single-tap alternative: +/− steppers beside each diagram handle, tap-to-jump on the timeline, and "Step back" and "Step forward" buttons |
| 2.5.8 Target size | All targets are at least 48 by 48 dp, well above the 24 by 24 minimum |
| 3.2.6 Consistent help | "Help and glossary" sits in the same place (the You menu) on every screen |
| 3.3.7 Redundant entry | Order tickets remember the last quantity and order type; quiz retakes never ask for anything again |
| 3.3.8 Accessible authentication | Sign in with Apple, Google or an email link; no passwords to recall and no puzzles |
| 4.1.2 Name, role, value | Each custom painter supplies semantics (below) |

**Charts for screen readers.** Every `CustomPainter` implements `semanticsBuilder`, and every chart has a text summary that a screen reader reads first: "Covered call on SPY. Max gain $640 above $105. Breakeven $98.60. Loses below breakeven, up to $9,860 if the stock falls to zero." Diagram handles are adjustable semantics nodes, so VoiceOver and TalkBack users swipe up or down to move price, strike or days left and hear the new values. Long charts offer "Read data as a table". On the web, the app calls `SemanticsBinding.instance.ensureSemantics()` at startup so the accessibility tree is always on, rather than waiting for the hidden enable button Flutter web shows by default.

**Other access needs.** Respect system bold text, reduce motion, high contrast and color inversion; support switch control and external keyboards on iPad and Android; caption any lesson video and avoid audio-only content; and keep reading level near grade 7 for lesson text, checked with a readability tool in the copy pipeline (**Proposed**).

**Teen safety as design rules.** The spec's teen duties shape screens, not only settings. For learners under 18:

- **Streaks are off by default** and shown only after a learner turns them on in Settings; when off, nothing hints at a streak.
- **Notifications** never arrive between 9 PM and 8 AM local time and never more than once a day; the permission prompt appears only from a tap, never at first launch.
- **The break prompt** appears after 45 minutes of continuous play as a calm sheet with two equal buttons.
- **No autoplay of the next replay**, no infinite feeds, no variable rewards, no countdowns that rush a trade, and no "you'll lose your streak" warnings.
- **Identity stays private**: generated nickname only, no photo, no location, a "Hide me from the global board" switch right on the leaderboard, and no outbound share buttons anywhere (the spec's "no sharing").
- **Rewards honor process**: badges for passing a challenge within its risk rule and for finishing lessons, never for the size of a profit; leaderboard scores are risk-adjusted, as the spec says.
- **No real-money cues**: no broker logos, links, referrals or "open an account" prompts, and no imagery of cash, cars or luxury.

These rules apply to everyone where they cost nothing (no autoplay, no rushed trades, no profit-size rewards), and to under-18s where the spec makes them teen defaults (streaks, notifications, break prompt, hiding).

## Responsive layouts, PWA and native

One Flutter codebase, one design system, three platforms: the look is identical everywhere, while gestures, system controls and input follow each platform's habits. Layout follows Material 3 window size classes, read once per frame from `MediaQuery.sizeOf`.

| Width class | Width (dp) | Navigation | Lesson | Replay and live | Trade ticket |
| --- | --- | --- | --- | --- | --- |
| Compact | under 600 | Bottom nav bar | Text above diagram, diagram sticky while reading | Chart full width, positions below | Bottom sheet, full height |
| Medium | 600 to 839 | Nav rail | Text and diagram side by side in landscape | Chart plus a collapsible positions panel | Bottom sheet, 70% height |
| Expanded | 840 to 1199 | Nav rail with labels | Two panes: text left, diagram right | Chart left, positions and orders right | Side panel, 360 dp |
| Large | 1200 and up | Navigation drawer | Two panes, max line length 72 characters | Three panes: watchlist, chart, ticket | Always-open side panel |

Content never stretches past 1,440 dp; wider windows center it.

**The web app (PWA)**, set up the way the spec describes:

- **Install.** The manifest uses standalone display, the dark `surface` as theme and background color, and maskable icons. Chrome shows its own install prompt; on iPhone and iPad an "Install the app" sheet shows the three Add to Home Screen steps with pictures, offered once after the first finished lesson, never on first visit (**Proposed** timing).
- **First load.** `index.html` shows a light HTML splash with the logo and a progress line while the Flutter bundle loads, so the screen is never blank; the budget is a visible splash within 1 second and an interactive home within 3 seconds on a mid-range phone over 4G (**Proposed**).
- **Offline.** Cached scenario packs play offline in the installed app; screens that need the network (live market, leaderboards, debriefs) show what still works and queue results to sync.
- **Push.** Web push only after install on iOS, asked from a tap in Settings or after a weekly challenge, with the same quiet hours as mobile.
- **Links and history.** Every lesson, scenario, ticker and debrief has a URL from go\_router; the browser back button works; each route sets the tab title ("Lesson 2.5: The covered call").
- **Pointer and keyboard.** Hover shows crosshairs and rich tooltips; lesson text is selectable (`SelectionArea`); browser zoom to 200% reflows; keyboard shortcuts cover the spec's orders and replay speed (below).
- **Disclaimer and age gate.** The landing page shows the 13+ gate and "simulated money, no real trading" before signup, and every screen carries the short disclaimer in its footer.

**Keyboard shortcuts on the web** (**Proposed** keys). Single-key shortcuts work only while the chart or ticket has focus and can be turned off in Settings, which meets WCAG 2.1.4.

| Key | Action |
| --- | --- |
| Space | Play or pause the replay |
| ← / → | Step one bar back or forward (Shift: ten bars) |
| 1, 2, 3 | Replay speed: 1 day per 60, 30 or 10 seconds |
| B / S | Open the ticket on Buy or Sell |
| Enter | Review, then place, the order in the ticket |
| Esc | Close the sheet or panel |
| ? | Show all shortcuts |

**Native differences** (iOS and Android)

- **Navigation gestures:** iOS edge-swipe back and Android predictive back both work on every pushed screen; neither can drop an unplaced order without the "Discard order?" check.
- **Sign-in buttons** follow Apple's and Google's own button rules (logos, labels, sizes), the one place the custom theme yields to platform brand rules.
- **Text and motion settings:** Dynamic Type, Android font scale, bold text and reduce motion are read live.
- **Scroll physics:** bouncing on iOS, clamping with stretch on Android; the custom design is otherwise identical.
- **Haptics:** only on native, as listed in Motion.
- **System sheets:** native date picker for the birthdate gate; no share sheet anywhere, because the spec allows no sharing.
- **App icon and splash:** adaptive icon on Android, a single icon on iOS, and a splash that matches the web splash.

## Proposed decisions and open questions

Everything above that the spec had not already settled is marked Proposed; this table collects those decisions so each can be accepted or changed in one place.

| # | Proposed decision | Why |
| --- | --- | --- |
| 1 | Brand primary is violet (#B3A6FF dark, #5B43D6 light) and never appears inside charts | Keeps blue and orange free to mean gain and loss |
| 2 | Buy and Sell use the same neutral brand styles, not green and red | Avoids teaching "selling is danger" and "buying is profit" |
| 3 | Level icons Seed, Sprout, Stalk, Harvest | Reuses the farm analogy without new colors |
| 4 | Space Grotesk for headlines, Inter with tabular figures for everything else, bundled | Distinct, readable, offline and no third-party font requests |
| 5 | Lesson text at 18/28 | Comfortable reading for 3 to 5 minute lessons |
| 6 | Five destinations: Learn, Replays, Live, Challenges, Portfolio | Matches the core loop; see Navigation |
| 7 | "Match system" theme option beside the dark default | Some learners study in bright rooms |
| 8 | Compact chain shows one side at a time with a Calls/Puts switch | Both sides do not fit legibly at 360 dp |
| 9 | iOS install sheet after the first finished lesson | Asks once the learner has seen value |
| 10 | Web keys Space, arrows, 1 to 3, B, S, Enter, Esc, ? | Covers the spec's "shortcuts for orders and replay speed" |
| 11 | Light haptics for snaps and fills only | Feedback without rewarding profit |
| 12 | Sign-in button order: Apple first on iOS, Google first elsewhere | Platform expectation |
| 13 | Web budget: splash within 1 s, interactive within 3 s on mid-range 4G | Flutter web loads a large bundle; the splash covers it |
| 14 | Grade 7 reading level for lessons | Fits 13-year-olds and busy adults |

Open questions:

- **Name and logo.** The guide uses no logo yet; the mark waits for Ticker Camp, or another name, to clear trademark review.
- **Illustration style.** Lessons rely on diagrams, so the guide adds no illustrations; a small set of farm spot illustrations for empty states is possible later.
- **Design files.** The next step is a Figma (or Flutter widgetbook) library built from these tokens, and the 10 screens as high-fidelity mocks, before code starts.
- **Usability tests.** Five teens and five adults should try onboarding, one lesson and the March 2020 replay on phones before launch.
