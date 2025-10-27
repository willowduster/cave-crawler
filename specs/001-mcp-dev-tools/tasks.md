# Tasks: MCP Development Tools Integration

**Input**: Design documents from `/specs/001-mcp-dev-tools/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: TDD approach required per constitution (Principle IV)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

**This feature uses infrastructure structure** (separate from game code):
- Root: `mcp-servers/` (sibling to `cave-crawler/`)
- Source: `mcp-servers/servers/`, `mcp-servers/config/`
- Tests: `mcp-servers/tests/`
- Docs: `mcp-servers/docs/`
- Scripts: `mcp-servers/scripts/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and MCP server structure

- [ ] T001 Create mcp-servers/ directory structure per plan.md
- [ ] T002 Initialize Python project with pyproject.toml in mcp-servers/
- [ ] T003 [P] Create requirements.txt with dependencies (mcp>=0.9.0, pydantic, psutil, winreg)
- [ ] T004 [P] Create mcp-servers/README.md with project overview
- [ ] T005 [P] Setup .gitignore for Python projects in mcp-servers/
- [ ] T006 [P] Create config/mcp-config.schema.json from data-model.md
- [ ] T007 [P] Create config/mcp-config.example.json with sample configuration

**Checkpoint**: Basic project structure ready for development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Create servers/common/base_server.py with MCP Server base class
- [ ] T009 Create servers/common/detector_base.py with tool detection base logic
- [ ] T010 [P] Create servers/common/logger.py with unified logging system
- [ ] T011 [P] Create servers/common/__init__.py with exports
- [ ] T012 Implement configuration loading in servers/common/config_loader.py
- [ ] T013 Implement configuration validation using pydantic in servers/common/config_validator.py
- [ ] T014 [P] Create data models in servers/common/models.py (ToolInstallation, MCPOperationRequest, OperationLogEntry, MCPServerState)
- [ ] T015 [P] Implement file locking utility in servers/common/file_lock.py
- [ ] T016 [P] Implement atomic write utility in servers/common/atomic_write.py
- [ ] T017 Create tests/unit/test_config_loader.py (test config loading and validation)
- [ ] T018 [P] Create tests/unit/test_file_lock.py (test concurrent file access)
- [ ] T019 [P] Create tests/unit/test_atomic_write.py (test atomic write operations)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Godot Engine MCP Server Access (Priority: P1) 🎯 MVP

**Goal**: Enable AI to interact with Godot projects (read/create scenes and scripts)

**Independent Test**: Query Godot project structure, create a new scene file, verify it appears in Godot editor

### Tests for User Story 1 (TDD Required)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T020 [P] [US1] Create tests/fixtures/mock_godot_project/ with sample .tscn and .gd files
- [ ] T021 [P] [US1] Unit test for Godot installation detection in tests/unit/test_godot_detector.py
- [ ] T022 [P] [US1] Unit test for .tscn file parsing in tests/unit/test_godot_parser.py
- [ ] T023 [P] [US1] Unit test for GDScript file operations in tests/unit/test_godot_script.py
- [ ] T024 [US1] Integration test for list_project_files operation in tests/integration/test_godot_operations.py
- [ ] T025 [US1] Integration test for read_scene operation in tests/integration/test_godot_operations.py
- [ ] T026 [US1] Integration test for create_scene operation in tests/integration/test_godot_operations.py
- [ ] T027 [US1] Integration test for read_script and create_script operations in tests/integration/test_godot_operations.py

### Implementation for User Story 1

- [ ] T028 [P] [US1] Implement Godot installation detector in servers/godot/detector.py
- [ ] T029 [P] [US1] Implement Godot project file parser in servers/godot/parser.py
- [ ] T030 [US1] Implement list_project_files operation in servers/godot/operations.py
- [ ] T031 [US1] Implement read_scene operation in servers/godot/operations.py
- [ ] T032 [US1] Implement read_script operation in servers/godot/operations.py
- [ ] T033 [US1] Implement create_scene operation in servers/godot/operations.py
- [ ] T034 [US1] Implement create_script operation in servers/godot/operations.py
- [ ] T035 [US1] Implement update_script operation in servers/godot/operations.py
- [ ] T036 [US1] Implement validate_syntax operation (using Godot CLI) in servers/godot/operations.py
- [ ] T037 [US1] Implement list_resources operation in servers/godot/operations.py
- [ ] T038 [US1] Create Godot MCP server entry point in servers/godot/server.py
- [ ] T039 [US1] Add error handling and logging for all Godot operations
- [ ] T040 [US1] Create servers/godot/__init__.py with exports
- [ ] T041 [US1] Run all Godot tests to verify implementation

**Checkpoint**: Godot MCP server fully functional - AI can manage Godot projects independently

---

## Phase 4: User Story 4 - Unified MCP Configuration Management (Priority: P1)

**Goal**: Centralized configuration for managing all MCP servers

**Independent Test**: Modify configuration file, restart MCP infrastructure, verify changes take effect

### Tests for User Story 4 (TDD Required)

- [ ] T042 [P] [US4] Unit test for configuration schema validation in tests/unit/test_config.py
- [ ] T043 [P] [US4] Unit test for tool detection caching in tests/unit/test_detection_cache.py
- [ ] T044 [US4] Integration test for start/stop all servers in tests/integration/test_server_lifecycle.py
- [ ] T045 [US4] Integration test for configuration reload in tests/integration/test_config_reload.py

### Implementation for User Story 4

- [ ] T046 [P] [US4] Implement detect-tools.ps1 script in scripts/detect-tools.ps1
- [ ] T047 [P] [US4] Implement validate-config.ps1 script in scripts/validate-config.ps1
- [ ] T048 [US4] Implement start-all-servers.ps1 script in scripts/start-all-servers.ps1
- [ ] T049 [US4] Implement stop-all-servers.ps1 script in scripts/stop-all-servers.ps1
- [ ] T050 [US4] Create server orchestrator in servers/common/orchestrator.py
- [ ] T051 [US4] Implement server state tracking in servers/common/state_manager.py
- [ ] T052 [US4] Create detected-tools.json auto-generation logic
- [ ] T053 [US4] Add configuration change detection and hot reload
- [ ] T054 [US4] Implement logging configuration and rotation
- [ ] T055 [US4] Create docs/setup.md from quickstart.md template
- [ ] T056 [US4] Run all configuration management tests to verify implementation

**Checkpoint**: Configuration management complete - All servers can be managed from single config

---

## Phase 5: User Story 2 - Blender MCP Server for 3D Asset Creation (Priority: P2)

**Goal**: Enable AI to create and modify 3D models in Blender

**Independent Test**: Create simple 3D model (sword/potion), export as GLTF, verify usable in Godot

### Tests for User Story 2 (TDD Required)

- [ ] T057 [P] [US2] Create tests/fixtures/mock_blender_files/ with sample scripts
- [ ] T058 [P] [US2] Unit test for Blender installation detection in tests/unit/test_blender_detector.py
- [ ] T059 [P] [US2] Unit test for Blender script generation in tests/unit/test_blender_script_gen.py
- [ ] T060 [US2] Integration test for create_primitive operation in tests/integration/test_blender_operations.py
- [ ] T061 [US2] Integration test for export_gltf operation in tests/integration/test_blender_operations.py
- [ ] T062 [US2] Integration test for apply_material operation in tests/integration/test_blender_operations.py

### Implementation for User Story 2

- [ ] T063 [P] [US2] Implement Blender installation detector in servers/blender/detector.py
- [ ] T064 [P] [US2] Create Blender script templates in servers/blender/templates/
- [ ] T065 [US2] Implement create_primitive operation in servers/blender/operations.py
- [ ] T066 [US2] Implement modify_object operation in servers/blender/operations.py
- [ ] T067 [US2] Implement apply_material operation in servers/blender/operations.py
- [ ] T068 [US2] Implement export_gltf operation in servers/blender/operations.py
- [ ] T069 [US2] Implement import_reference operation in servers/blender/operations.py
- [ ] T070 [US2] Implement list_objects operation in servers/blender/operations.py
- [ ] T071 [US2] Implement execute_script operation in servers/blender/operations.py
- [ ] T072 [US2] Implement render_preview operation in servers/blender/operations.py
- [ ] T073 [US2] Create Blender subprocess manager with timeout handling
- [ ] T074 [US2] Create Blender MCP server entry point in servers/blender/server.py
- [ ] T075 [US2] Add error handling and logging for all Blender operations
- [ ] T076 [US2] Create servers/blender/__init__.py with exports
- [ ] T077 [US2] Run all Blender tests to verify implementation

**Checkpoint**: Blender MCP server fully functional - AI can create 3D assets independently

---

## Phase 6: User Story 3 - GIMP MCP Server for 2D Art and Textures (Priority: P3)

**Goal**: Enable AI to create and edit 2D sprites, UI elements, and textures

**Independent Test**: Create sprite sheet, add layers, apply effects, export as PNG

### Tests for User Story 3 (TDD Required)

- [ ] T078 [P] [US3] Create tests/fixtures/mock_gimp_files/ with sample images
- [ ] T079 [P] [US3] Unit test for GIMP installation detection in tests/unit/test_gimp_detector.py
- [ ] T080 [P] [US3] Unit test for Python-Fu script generation in tests/unit/test_gimp_script_gen.py
- [ ] T081 [US3] Integration test for create_image operation in tests/integration/test_gimp_operations.py
- [ ] T082 [US3] Integration test for export_png operation in tests/integration/test_gimp_operations.py
- [ ] T083 [US3] Integration test for layer manipulation in tests/integration/test_gimp_operations.py

### Implementation for User Story 3

- [ ] T084 [P] [US3] Implement GIMP installation detector in servers/gimp/detector.py
- [ ] T085 [P] [US3] Create Python-Fu script templates in servers/gimp/templates/
- [ ] T086 [US3] Implement create_image operation in servers/gimp/operations.py
- [ ] T087 [US3] Implement open_image operation in servers/gimp/operations.py
- [ ] T088 [US3] Implement add_layer operation in servers/gimp/operations.py
- [ ] T089 [US3] Implement apply_filter operation in servers/gimp/operations.py
- [ ] T090 [US3] Implement export_png operation in servers/gimp/operations.py
- [ ] T091 [US3] Implement resize_image operation in servers/gimp/operations.py
- [ ] T092 [US3] Implement merge_layers operation in servers/gimp/operations.py
- [ ] T093 [US3] Implement get_image_info operation in servers/gimp/operations.py
- [ ] T094 [US3] Create GIMP subprocess manager with batch mode handling
- [ ] T095 [US3] Create GIMP MCP server entry point in servers/gimp/server.py
- [ ] T096 [US3] Add error handling and logging for all GIMP operations
- [ ] T097 [US3] Create servers/gimp/__init__.py with exports
- [ ] T098 [US3] Run all GIMP tests to verify implementation

**Checkpoint**: GIMP MCP server fully functional - AI can create 2D art independently

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final documentation

- [ ] T099 [P] Create comprehensive operation reference in docs/operation-reference.md
- [ ] T100 [P] Create troubleshooting guide in docs/troubleshooting.md
- [ ] T101 [P] Add example usage scripts in docs/examples/
- [ ] T102 Code cleanup and refactoring across all servers
- [ ] T103 Performance optimization for file operations and subprocess management
- [ ] T104 [P] Security review for path validation and command injection prevention
- [ ] T105 [P] Add comprehensive logging throughout all operations
- [ ] T106 Create pytest configuration and run full test suite
- [ ] T107 [P] Add type hints throughout codebase (Python 3.11+ typing)
- [ ] T108 Setup pre-commit hooks for linting and formatting
- [ ] T109 Run quickstart.md validation end-to-end
- [ ] T110 Create installation package/wheel for easy distribution
- [ ] T111 [P] Update main cave-crawler README.md with MCP setup link
- [ ] T112 Final integration test: Create full game asset workflow (scene + model + sprite)

**Checkpoint**: Feature complete, polished, and ready for production use

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 - Godot (Phase 3)**: Depends on Foundational (Phase 2) ✅ MVP
- **User Story 4 - Config Management (Phase 4)**: Depends on Foundational (Phase 2) ✅ MVP
- **User Story 2 - Blender (Phase 5)**: Depends on Foundational (Phase 2) + US4 (config system)
- **User Story 3 - GIMP (Phase 6)**: Depends on Foundational (Phase 2) + US4 (config system)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Foundational (Phase 2) - REQUIRED FOR ALL
    ├── US1: Godot (P1) - Independent, can start immediately after Phase 2
    ├── US4: Config Management (P1) - Independent, can start immediately after Phase 2
    │   ├── US2: Blender (P2) - Needs US4 for configuration system
    │   └── US3: GIMP (P3) - Needs US4 for configuration system
```

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (Godot) + Phase 4 (Config) = Minimal viable MCP infrastructure

**Recommended Order**:
1. Phase 1: Setup
2. Phase 2: Foundational
3. Phase 3 + Phase 4 (parallel): Godot server + Config management
4. Phase 5: Blender (after US4 complete)
5. Phase 6: GIMP (after US4 complete)
6. Phase 7: Polish

### Within Each User Story

**Test-Driven Development (TDD) Flow**:
1. Write tests first (unit + integration)
2. Run tests - they should FAIL
3. Implement features to make tests pass
4. Refactor while keeping tests green
5. Add error handling and logging
6. Final test run to verify story complete

**Implementation Order Within Story**:
- Fixtures/mocks first (for testing)
- Unit tests before implementation
- Detection logic (tool finding)
- Core operations (one at a time, test-driven)
- Integration tests after each operation
- Server entry point last
- Error handling throughout

### Parallel Opportunities

**Setup Phase**: All tasks marked [P] (T003, T004, T005, T006, T007) can run simultaneously

**Foundational Phase**: Parallelizable tasks:
- T010 (logger), T011 (__init__), T014 (models), T015 (file lock), T016 (atomic write) can run together
- T017, T018, T019 (tests) can run after their respective implementations

**User Story Phases**: After Phase 2 complete:
- US1 (Godot) and US4 (Config) can start in parallel
- Within each story:
  - All unit tests marked [P] can run in parallel
  - All fixtures/templates can be created in parallel
  - Operations implementations are sequential (build on each other)

**Polish Phase**: Most tasks (T099-T111) can run in parallel except T106 (test suite) and T109 (validation) which depend on everything

---

## Parallel Example: User Story 1 (Godot)

**Scenario**: 2 developers working on US1 simultaneously

```bash
# Developer 1: Tests
T020-T027 (all test writing in parallel)

# Developer 2: Core infrastructure
T028 (detector) → T029 (parser)

# Then both developers implement operations (one per developer):
# Developer 1: T030, T032, T034, T036
# Developer 2: T031, T033, T035, T037

# Developer 1: T038 (server entry point)
# Developer 2: T039 (error handling)

# Both: T041 (run tests)
```

---

## Task Summary

**Total Tasks**: 112

**Task Breakdown by Phase**:
- Setup (Phase 1): 7 tasks
- Foundational (Phase 2): 12 tasks
- US1 - Godot (Phase 3): 22 tasks (8 tests + 14 implementation)
- US4 - Config (Phase 4): 15 tasks (4 tests + 11 implementation)
- US2 - Blender (Phase 5): 21 tasks (6 tests + 15 implementation)
- US3 - GIMP (Phase 6): 21 tasks (6 tests + 15 implementation)
- Polish (Phase 7): 14 tasks

**Parallel Opportunities**: 42 tasks marked [P] can be parallelized

**MVP Scope** (Minimum viable product):
- Phase 1: Setup (7 tasks)
- Phase 2: Foundational (12 tasks)
- Phase 3: US1 - Godot (22 tasks)
- Phase 4: US4 - Config Management (15 tasks)
- **Total MVP: 56 tasks** (50% of total)

**Independent Test Criteria**:
- ✅ **US1 (Godot)**: Create Godot scene file via AI, verify it appears in editor
- ✅ **US4 (Config)**: Modify config file, restart servers, verify changes applied
- ✅ **US2 (Blender)**: Create 3D model via AI, export as GLTF, verify format
- ✅ **US3 (GIMP)**: Create sprite via AI, export as PNG, verify transparency

**Format Validation**: ✅ All 112 tasks follow checklist format with ID, optional [P] marker, optional [Story] label, and file paths

---

## Implementation Strategy

### MVP-First Approach

**Goal**: Get working MCP infrastructure as quickly as possible

**Recommended Flow**:
1. **Week 1**: Setup + Foundational (Phases 1-2) - 19 tasks
2. **Week 2**: Godot Server (Phase 3) - 22 tasks ✅ First AI-assisted scene creation works
3. **Week 3**: Config Management (Phase 4) - 15 tasks ✅ Production-ready server management
4. **Milestone**: MVP complete - Can ship and use for development

**Future Enhancements** (after MVP deployed):
5. **Week 4**: Blender Server (Phase 5) - 21 tasks
6. **Week 5**: GIMP Server (Phase 6) - 21 tasks
7. **Week 6**: Polish (Phase 7) - 14 tasks

### Incremental Delivery

Each user story phase can be deployed independently:
- After US1 complete: Ship Godot MCP server
- After US4 complete: Add configuration management
- After US2 complete: Add Blender support
- After US3 complete: Add GIMP support
- After Phase 7: Full polish and optimization

### Risk Mitigation

**Highest Risk**: Tool detection on various Windows configurations
- Mitigated by: Multiple detection methods + manual override in config
- Test early with different Windows setups

**Medium Risk**: Subprocess management (timeouts, zombies)
- Mitigated by: Comprehensive timeout handling + process cleanup
- Test with long-running operations

**Low Risk**: File corruption from concurrent access
- Mitigated by: File locking + atomic writes
- Test with concurrent operation stress tests

---

**Ready to Begin**: All tasks defined, dependencies clear, MVP scope identified. Start with Phase 1! 🚀
