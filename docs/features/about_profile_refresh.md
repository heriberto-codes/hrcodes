# About Profile Refresh

## Summary

- Updated the live About résumé link and the historical About mockup to the owner-supplied [November 2026 PDF](https://hroman-codes.s3.us-east-2.amazonaws.com/HRomandevresume_November_2026.pdf).
- Added “Current student · Boston University” and “Master’s in Software Engineering for Artificial Intelligence” beneath the existing portrait role and name.
- Both steps in the [implementation plan](../plans/about_profile_refresh_plan.md) completed EXECUTE, VERIFY, ENGINEER CHECKPOINT, TEST, and PLAN STEP UPDATE. The matching [backlog item](../backlog.md) is checked. No DEBUG repair was required.

## Architecture Impact

- Retained the existing Django homepage/include boundary. Application changes are confined to `templates/includes/about.html`, `static/pages/home.css`, and the CSS query version in `templates/home.html`.
- No API, database, view, query, dependency, or JavaScript changes. Inquiry validation, CSRF protection, throttling, authentication, and Sentry privacy controls are unchanged.

## Decisions

- Followed the approved [Continuity — current studies design](../design/about_profile_refresh/approved-design.md), preserving the portrait, role/name order, surrounding About content, desktop sticky column, and mobile stacking.
- Used static paragraphs, existing color tokens, a fine divider, and natural wrapping. Added no graduation date, completed-degree claim, fixed caption height, truncation, or new breakpoint.
- Replaced the complete S3 destination because its bucket, region, and filename changed. Preserved the live link’s visible label, hidden new-tab announcement, `target="_blank"`, and `rel="noopener noreferrer"`.
- Changed only the historical mockup’s résumé destination, retaining its `download="Heriberto-Roman-Resume.pdf"` attribute and existing design.
- Refreshed the homepage CSS query version to `20261122-about-profile-1`; the JavaScript version is unchanged.

## Test Impact

- Extended two existing tests in `apps/pages/tests/test_views.py`: the About semantic/destination contract and the page-scoped foundation contract. Coverage checks the exact November URL, rejection of the old URL, preserved link semantics, both education statements appearing once inside the caption after role/name, and the updated CSS version.
- Final validation passed: 2 targeted tests, all 46 view tests, and all 146 repository tests. The full suite used the ten explicit module labels listed in the plan because default discovery has a known limitation. Django configuration checks succeeded with the existing CKEditor warning; whitespace checks passed.
- Actual Django homepage browser checks covered 320, 390, 768, 1000, and 1440px widths. The portrait decoded, the full program title wrapped without education/document overflow at normal text size, and desktop/mobile ordering matched the design. Desktop and mobile caption captures were compared with approved previews.
- At desktop widths with a 600px-tall viewport, the column retained its sticky position and the complete education block remained reachable near the section’s end. Keyboard Tab navigation reached the résumé link with visible focus and its new-tab announcement intact.
- At 200% root text size, the education block had no horizontal overflow. Existing document overflow at 320, 390, and 768px remained unchanged when the new block was temporarily hidden in the browser.
- VERIFY and ENGINEER CHECKPOINT passed for both steps. Security and performance reviews found no actionable issues in scope; an independent delegated branch review also returned no actionable findings. These results come from the completed workflow and were not rerun during documentation.

## Deployment Notes

- No deployment or migration was performed; no new environment variables are required.
- Generated `staticfiles/` output was not edited. The production change adds no new image, script, or remote embed.

## Follow-ups / Accepted Risks

- Remote PDF availability, contents, and S3 permissions remain unverified. The supplied URL is linked directly; this record does not establish that the remote document loads or contains the intended résumé.
- Native browser zoom, real-device, and screen-reader checks remain unverified. The 200% root text checks establish text-enlargement behavior only.
- Existing narrow-width overflow with enlarged text, the tall sticky column in short windows, test discovery limitations, and the CKEditor warning remain outside this feature’s scope.
- The performance review inspected source changes; production load timings were not benchmarked.
