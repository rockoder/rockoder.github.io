---
title: "Software Design Document Template"
date: 2016-07-16T23:04:00.003+05:30
author: "Ganesh Pagade"
tags: ["programming", "documentation"]
draft: false
---

Many organizations, new and old, struggle to come up with a descent Software Design Document Template for the teams to follow. I plan to provide a template with various sections that could be considered while working on the software design. Not all sections may be applicable for each feature. Developer/Architect should pick up the relevant sections.

# Contents

* [1. Introduction](#1-introduction)
* [2. Related Documents](#2-related-documents)
* [3. Definitions](#3-definitions)
* [4. Limitations of Current Product Functionality and Architecture](#4-limitations-of-current-product-functionality-and-architecture)
* [5. Solution Highlight](#5-solution-highlight)
* [6. Acceptance Criteria](#6-acceptance-criteria)
* [7. Functional Design](#7-functional-design)
* [8. Architecture](#8-architecture)
* [9. Implementation Design](#9-implementation-design)
* [10. Development Considerations](#10-development-considerations)
* [11. External Dependencies, Blockers and Risks](#11-external-dependencies-blockers-and-risks)
* [12. Approvals](#12-approvals)

# 1. Introduction
Provide context for this architectural change or new feature.

# 2. Related Documents
Point to related User Stories in AGM, defects, wiki pages, research/approach wiki/docs, attachments (PPTs, Docs).

# 3. Definitions
Terminologies, Acronyms and their meaning, description etc.

# 4. Limitations of Current Product Functionality and Architecture
Limitations, Drawbacks, Defects, Issues etc. in existing product before implementing this feature/story.

# 5. Solution Highlight
Executive summary of architectural changes and/or new features. Along with section 4 (above), the reader should be able to understand the problem being solved, business context of the problem and how it is intended to be solved.

# 6. Acceptance Criteria
Identify the acceptance test criteria. This could include development test suite, smoke tests suite etc.

# 7. Functional Design
Use this section on highlight WHAT functionality is to be introduced/changed within the product. Provide details about the use cases, actors, scope etc. Below two sections combined should be able to capture clear understanding of the functionality from engineering point of view.

- Itemized Functionality

	Describe each new functionality to be introduced, explaining how an use case would be achieved.

- User Visible Changes
	- GUI Changes

		Use mock ups, screenshots, wire frames to show new GUI to be implemented. Highlight new changes in comparison to old GUI. Include error/warning/validation messages.

	- CLI Changes

		Describe CLI additions/changes, syntax changes, options/parameters meaning, environment variables (if any), input, output, error messages etc.

	- API Changes

		Describe additions/changes to any public APIs like REST etc.

	- Configuration Changes

		Describe changes to customer visible configuration file changes.

	- Installer Considerations

		Identify new screens/cli questions to take input from the user during installation. Identify new directories and files that will be introduced and there location within installer and application. Also describe config files/registry settings/environment variables changes that would take place. Need for system/component reboot etc.

	- Documentation Changes
	
		Identify documents that needs to be updated and brief summary of the changes.

# 8. Architecture
High level architectural changes. Highlight what changes will be introduced as compared to existing architecture using old/new diagrams or colors/sections within the diagram. Following diagrams, as appropriate, can be used:
	
- Context diagram

	A very high-level diagram showing your system as a box in the center, surrounded by other boxes representing the users and all of the other products/systems that the software system interfaces with.

- Container diagram

	A high-level diagram showing the various web servers, application servers, standalone applications, databases, file systems, etc that make up your software system, along with the relationships/interactions between them.

- Block/Component diagram

	One per container, showing major components and their relationships.

# 9. Implementation Design
	
- Domain Model Design
	
	Relatively detailed design of the code/solution. Explain new classes introduced, classes which underwent major changes, design patterns used etc. Following diagrams, as appropriate, can be used:

	- Class Diagram

		Explaining implementation of particular component. Also can be used to explain design patterns and future extensibility.

	- Collaboration Diagram

		Showing high level communication between objects.

	- Sequence Diagram

		Showing complex interactions between objects over time.

- Data Model Design
	
	Relatively detailed design of the new tables/columns. Explain purpose of each table/column, when/who/how of CRUD operations, normalization considerations etc. Also mention affected files (sql, xml, scripts). Following diagrams, as appropriate, can be used:

	- Entity Relationship Diagram

		Showing relationship between the new tables/columns introduced.

	- CRUD Table

		Chart showing CRUD operations performed by various processes on entities.

# 10. Development Considerations
- Deployment

	Describe hardware, system requirements and other deployment configurations like ports opened, firewalls etc.

- Upgrade

	Describe upgrade steps and files affected. Consider existing configuration files and data during upgrade. Also consider backup and rollback action plan.

- Migration

	Describe database migration plan. Explain tables affected, steps for migrations and scripts/tools involved. Also consider backup and rollback action plan.

- Import/Export

- Reports

- Compatibility

- Scalability and Performance

- Security

- Internationalization

# 11. External Dependencies, Blockers and Risks

# 12. Approvals

- Dev Manager

- QA Manager

- Product Owner

- Tech Pub Manager

- Solution Architect

- Product Architect

- Support Manager

- UX Manager
