# Tasks: Greet CLI - Multilingual Hello World Tool

**Input**: Design documents from `/specs/001-greet-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in the feature specification. Tests may be added later.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Python package: `src/greet/`
- Renderers subpackage: `src/greet/renderers/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and basic structure

- [ ] T001 Initialize Python project with pyproject.toml including Click, Rich, pyfiglet dependencies
- [ ] T002 [P] Create src/greet/__init__.py with package version
- [ ] T003 [P] Create src/greet/renderers/__init__.py for renderers subpackage
- [ ] T004 [P] Configure pyproject.toml with CLI entry point `greet = "greet.cli:main"`
- [ ] T005 [P] Create tests/conftest.py with shared fixtures
- [ ] T006 Run `uv sync` to install all dependencies and verify setup
- [ ] T006b Verify CLI entry point works by running `uv run greet --help` (validates FR-018)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structures and shared utilities that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Create Language dataclass in src/greet/languages.py with code, name, banner_name, greeting_template, flag_emoji fields
- [ ] T008 Populate LANGUAGES list with all 10 languages (English, French, Spanish, German, Japanese, Mandarin, Arabic, Hindi, Swahili, Portuguese) in src/greet/languages.py
- [ ] T009 [P] Create Proverb dataclass in src/greet/fortunes.py with text, language, translation fields
- [ ] T010 [P] Populate PROVERBS list with 10-20 multilingual sayings in src/greet/fortunes.py
- [ ] T011 Create OutputConfig dataclass in src/greet/core.py with all CLI options as fields
- [ ] T012 Create Greeting dataclass in src/greet/core.py with language, text, banner fields
- [ ] T013 Implement generate_greeting function in src/greet/core.py that substitutes name into greeting_template
- [ ] T014 Create basic Click CLI skeleton in src/greet/cli.py with main command and --help/--version options

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Basic Multilingual Greeting Display (Priority: P1) 🎯 MVP

**Goal**: Display "Hello, World!" in all 10 languages with ASCII art banners and colors

**Independent Test**: Run `greet` with no arguments and verify all 10 languages display with banners

### Implementation for User Story 1

- [ ] T015 [US1] Implement render_figlet_banner function in src/greet/renderers/figlet.py using pyfiglet
- [ ] T016 [US1] Create Rich Console wrapper in src/greet/output.py with color support
- [ ] T017 [US1] Implement generate_all_greetings function in src/greet/core.py that creates Greeting objects for all languages
- [ ] T018 [US1] Implement render_greeting function in src/greet/output.py that outputs banner + colored greeting
- [ ] T019 [US1] Implement render_all_greetings function in src/greet/output.py that renders all greetings sequentially
- [ ] T020 [US1] Wire up CLI main command in src/greet/cli.py to generate and render all greetings with default options
- [ ] T021 [US1] Verify exit code 0 on successful execution in src/greet/cli.py

**Checkpoint**: User Story 1 complete - `greet` displays all 10 languages with figlet banners and colors

---

## Phase 4: User Story 2 - Filtered Language Selection (Priority: P1)

**Goal**: Allow users to filter output to specific languages with `--languages / -l`

**Independent Test**: Run `greet -l french,spanish` and verify only those languages appear

### Implementation for User Story 2

- [ ] T022 [US2] Add --languages/-l option to CLI in src/greet/cli.py accepting comma-separated string
- [ ] T023 [US2] Implement parse_language_filter function in src/greet/core.py to parse and validate language names
- [ ] T024 [US2] Implement get_language_by_name lookup function in src/greet/languages.py (case-insensitive)
- [ ] T025 [US2] Implement filter_languages function in src/greet/core.py that returns filtered Language list
- [ ] T026 [US2] Add error handling for invalid language names with helpful error message listing valid options in src/greet/cli.py
- [ ] T027 [US2] Set exit code 2 for invalid language errors in src/greet/cli.py

**Checkpoint**: User Story 2 complete - language filtering works with helpful error messages

---

## Phase 5: User Story 3 - Display Customization Options (Priority: P2)

**Goal**: Support `--no-figlet`, `--no-color`, and `--random` flags

**Independent Test**: Run with each flag and verify output changes accordingly

### Implementation for User Story 3

- [ ] T028 [P] [US3] Add --no-figlet flag to CLI in src/greet/cli.py
- [ ] T029 [P] [US3] Add --no-color flag to CLI in src/greet/cli.py
- [ ] T030 [P] [US3] Add --random flag to CLI in src/greet/cli.py
- [ ] T031 [US3] Update OutputConfig creation in src/greet/cli.py to include show_figlet, use_color, random_mode fields
- [ ] T032 [US3] Update Console initialization in src/greet/output.py to respect no_color setting
- [ ] T033 [US3] Update render_greeting in src/greet/output.py to conditionally skip figlet banner
- [ ] T034 [US3] Implement select_random_language function in src/greet/core.py
- [ ] T035 [US3] Update main CLI logic in src/greet/cli.py to handle random mode (single language output)

**Checkpoint**: User Story 3 complete - all display customization flags work

---

## Phase 6: User Story 4 - Personalized Greetings (Priority: P2)

**Goal**: Replace "World" with custom name using `--name NAME`

**Independent Test**: Run `greet --name Marie` and verify each language uses the name correctly

### Implementation for User Story 4

- [ ] T036 [US4] Add --name option to CLI in src/greet/cli.py with default "World"
- [ ] T037 [US4] Update OutputConfig in src/greet/core.py to include name field
- [ ] T038 [US4] Update generate_greeting function in src/greet/core.py to use name from OutputConfig
- [ ] T039 [US4] Verify special characters and spaces in names are preserved in src/greet/core.py

**Checkpoint**: User Story 4 complete - personalized greetings work in all languages

---

## Phase 7: User Story 5 - Fun Mode with Cowsay (Priority: P2)

**Goal**: Wrap output in cowsay-style speech bubble with ASCII animal

**Independent Test**: Run `greet --cowsay` and verify output is wrapped in speech bubble

### Implementation for User Story 5

- [ ] T040 [US5] Add --cowsay flag to CLI in src/greet/cli.py
- [ ] T041 [US5] Implement cowsay bubble generation in src/greet/renderers/cowsay.py with speech bubble and ASCII cow
- [ ] T042 [US5] Implement wrap_in_cowsay function in src/greet/renderers/cowsay.py that takes multiline text
- [ ] T043 [US5] Update render_all_greetings in src/greet/output.py to optionally wrap output in cowsay bubble
- [ ] T044 [US5] Verify cowsay works with --random flag in src/greet/cli.py

**Checkpoint**: User Story 5 complete - cowsay mode wraps all output in speech bubble

---

## Phase 8: User Story 6 - Party Mode (Priority: P3)

**Goal**: Enable party mode with confetti emojis, country flags, and randomized colors

**Independent Test**: Run `greet --party` and verify confetti, flags, and random colors appear

### Implementation for User Story 6

- [ ] T045 [US6] Add --party flag to CLI in src/greet/cli.py
- [ ] T046 [US6] Implement add_confetti function in src/greet/renderers/effects.py that adds emoji confetti
- [ ] T047 [US6] Implement random_color_style function in src/greet/renderers/effects.py for randomized colors
- [ ] T048 [US6] Update render_greeting in src/greet/output.py to include flag emoji when party mode enabled
- [ ] T049 [US6] Update render_greeting in src/greet/output.py to apply random colors in party mode
- [ ] T050 [US6] Verify party mode respects --no-color flag (flags shown, colors disabled) in src/greet/output.py

**Checkpoint**: User Story 6 complete - party mode adds festive visual effects

---

## Phase 9: User Story 7 - Fortune Quotes (Priority: P3)

**Goal**: Append random multilingual proverb after greetings with `--fortune`

**Independent Test**: Run `greet --fortune` and verify a proverb appears after greetings

### Implementation for User Story 7

- [ ] T051 [US7] Add --fortune flag to CLI in src/greet/cli.py
- [ ] T052 [US7] Implement select_random_proverb function in src/greet/fortunes.py
- [ ] T053 [US7] Implement render_fortune function in src/greet/output.py that displays proverb with optional translation
- [ ] T054 [US7] Update main CLI flow in src/greet/cli.py to append fortune after all greetings

**Checkpoint**: User Story 7 complete - fortune quotes add cultural wisdom

---

## Phase 10: User Story 8 - Grid Layout Display (Priority: P3)

**Goal**: Display greetings in grid layout with `--all-at-once`

**Independent Test**: Run `greet --all-at-once` and verify greetings appear in grid arrangement

### Implementation for User Story 8

- [ ] T055 [US8] Add --all-at-once flag to CLI in src/greet/cli.py
- [ ] T056 [US8] Implement render_grid_layout function in src/greet/output.py using Rich Columns or Table
- [ ] T057 [US8] Implement terminal width detection in src/greet/output.py for adaptive grid sizing
- [ ] T058 [US8] Update main CLI flow in src/greet/cli.py to use grid layout when --all-at-once enabled
- [ ] T059 [US8] Verify grid works with --cowsay (grid wrapped in single bubble) in src/greet/output.py

**Checkpoint**: User Story 8 complete - grid layout displays greetings compactly

---

## Phase 11: User Story 9 - Animated Output Modes (Priority: P3)

**Goal**: Support `--typewriter` and `--rainbow` animation effects

**Independent Test**: Run with each animation flag and observe visual effects

### Implementation for User Story 9

- [ ] T060 [P] [US9] Add --typewriter flag to CLI in src/greet/cli.py
- [ ] T061 [P] [US9] Add --rainbow flag to CLI in src/greet/cli.py
- [ ] T062 [US9] Implement typewriter_print function in src/greet/renderers/effects.py with character-by-character animation
- [ ] T063 [US9] Implement rainbow_print function in src/greet/renderers/effects.py with color cycling per character
- [ ] T064 [US9] Update render_greeting in src/greet/output.py to use animation effects when enabled
- [ ] T065 [US9] Implement combined typewriter + rainbow mode in src/greet/renderers/effects.py
- [ ] T066 [US9] Verify --rainbow respects --no-color flag (no colors applied) in src/greet/output.py

**Checkpoint**: User Story 9 complete - animations add dynamic visual effects

---

## Phase 12: User Story 10 - Decorative Box Mode (Priority: P3)

**Goal**: Draw Unicode box around each greeting with `--box`

**Independent Test**: Run `greet --box` and verify each greeting has a Unicode border

### Implementation for User Story 10

- [ ] T067 [US10] Add --box flag to CLI in src/greet/cli.py
- [ ] T068 [US10] Implement render_box function in src/greet/renderers/box.py using Rich Panel or manual Unicode box drawing
- [ ] T069 [US10] Update render_greeting in src/greet/output.py to wrap each greeting in box when enabled
- [ ] T070 [US10] Verify box works with --no-figlet (boxes shown, banners hidden) in src/greet/output.py

**Checkpoint**: User Story 10 complete - decorative boxes frame each greeting

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Final quality checks and improvements affecting multiple user stories

- [ ] T071 [P] Add comprehensive --help text for all options in src/greet/cli.py
- [ ] T072 [P] Verify all option combinations work without errors per cli-interface.md contract
- [ ] T073 Run `uv run ruff check` and fix any linting issues
- [ ] T074 Run `uv run ruff format` to ensure consistent code formatting
- [ ] T075 Run `uv run mypy --strict src/greet` and fix any type errors
- [ ] T076 Validate all quickstart.md examples work correctly
- [ ] T077 Verify performance: full output in <2 seconds (non-animated mode) per SC-001

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-12)**: All depend on Foundational phase completion
  - US1 (P1) and US2 (P1) should be completed first as MVP
  - US3-US5 (P2) can proceed after P1 stories
  - US6-US10 (P3) can proceed after P2 stories
- **Polish (Phase 13)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Depends only on Foundational - Core MVP, no other story dependencies
- **US2 (P1)**: Depends only on Foundational - Language filtering is independent
- **US3 (P2)**: Depends on US1 - Display options modify the base output
- **US4 (P2)**: Depends on US1 - Name personalization modifies greeting generation
- **US5 (P2)**: Depends on US1 - Cowsay wraps the output
- **US6 (P3)**: Depends on US1 - Party mode enhances the output
- **US7 (P3)**: Depends on US1, Foundational (Proverbs) - Fortune appends to output
- **US8 (P3)**: Depends on US1 - Grid is alternative layout for same content
- **US9 (P3)**: Depends on US1 - Animations modify how output is rendered
- **US10 (P3)**: Depends on US1 - Box wraps individual greetings

### Within Each User Story

- CLI option definition before implementation logic
- Core functions before output rendering
- Individual features before integration
- Verify feature works before marking complete

### Parallel Opportunities

**Setup Phase:**
- T002, T003, T004, T005 can run in parallel (different files)

**Foundational Phase:**
- T009, T010 (fortunes) can run parallel to T007, T008 (languages)

**User Story 3:**
- T028, T029, T030 can run in parallel (different CLI flags)

**User Story 9:**
- T060, T061 can run in parallel (different CLI flags)

**Polish Phase:**
- T071, T072 can run in parallel (documentation vs testing)

---

## Parallel Example: Setup Phase

```bash
# Launch all setup tasks together:
Task: "Create src/greet/__init__.py with package version"
Task: "Create src/greet/renderers/__init__.py for renderers subpackage"
Task: "Configure pyproject.toml with CLI entry point"
Task: "Create tests/conftest.py with shared fixtures"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Basic Greetings)
4. Complete Phase 4: User Story 2 (Language Filtering)
5. **STOP and VALIDATE**: Test both stories - `greet` and `greet -l french,spanish`
6. Deploy/demo if ready - this is a functional MVP!

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 + US2 (P1) → Test → Deploy (MVP with language filtering!)
3. US3 + US4 + US5 (P2) → Test → Deploy (Customization + Fun features)
4. US6 + US7 + US8 + US9 + US10 (P3) → Test → Deploy (Full feature set)
5. Polish → Final release

### Single Developer Strategy

Work through phases sequentially:
1. Setup → Foundational → US1 → US2 → (Validate MVP)
2. US3 → US4 → US5 → (Validate P2 features)
3. US6 → US7 → US8 → US9 → US10 → (Validate P3 features)
4. Polish → Done

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently testable after completion
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total: 78 tasks across 13 phases
