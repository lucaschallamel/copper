---
description: Run a mobile-development session , build or optimise native and cross-platform
  apps with platform polish, performance, and store readiness, grounded in the gd-mobile-app-developer
  skill (native, React Native, Flutter, OWASP MASVS).
---

Run a mobile-development session for: **$ARGUMENTS**

All arguments are optional. `platform` (default `cross-platform`; options: `ios`, `android`,
`cross-platform`, `react-native`, `flutter`); `app_type` (default `consumer`; options: `consumer`,
`enterprise`, `gaming`, `fintech`, `healthcare`); `optimization_focus` (default `performance`;
options: `performance`, `size`, `battery`, `ux`, `security`, `accessibility`); `complexity` (default
`standard`; options: `simple`, `standard`, `complex`, `enterprise`). With no arguments, ask what app
is being built and for which platform.

## Approach

1. **Load the mobile knowledge** , Use the `gd-development:mobile-app-developer` skill.
2. **Frame** , clarify the feature or app behind `$ARGUMENTS`, the target `platform` and `app_type`,
   and the OS-version and device range to support.
3. **Build** , apply the fitting architecture and state-management patterns for the `platform`, with
   60fps UI, secure storage (keychain/keystore), and platform integration as needed.
4. **Optimise and harden** , tune for the chosen `optimization_focus`, apply OWASP MASVS checks for
   sensitive data, validate accessibility, and prepare a store-ready release path.

## Examples

```text
# Enterprise fintech app on React Native
/gd-development:mobile-app-developer platform=react-native app_type=fintech complexity=enterprise

# Flutter app tuned for performance
/gd-development:mobile-app-developer platform=flutter optimization_focus=performance

# Complex iOS healthcare app
/gd-development:mobile-app-developer platform=ios app_type=healthcare complexity=complex
```

## Opening (when no args)

"Let's build a great mobile experience. What are you making, which platform (iOS, Android, or
cross-platform via React Native or Flutter), and what matters most , performance, size, battery, UX,
security, or accessibility?"

---

- Skill: `gd-development:mobile-app-developer` (owns the methodologies, the patterns, and the safety
  rules)
- Related agent: the proactive `gd-development:mobile-app-developer` agent loads the same skill autonomously.
