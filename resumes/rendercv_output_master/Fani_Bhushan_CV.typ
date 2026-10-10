// Import the rendercv function and all the refactored components
#import "@preview/rendercv:0.3.0": *

// Apply the rendercv template with custom configuration
#show: rendercv.with(
  name: "Fani Bhushan",
  title: "Fani Bhushan - CV",
  footer: context { [#emph[Fani Bhushan -- #str(here().page())\/#str(counter(page).final().first())]] },
  top-note: [ #emph[Last updated in June 2026] ],
  locale-catalog-language: "en",
  text-direction: ltr,
  page-size: "us-letter",
  page-top-margin: 0.7in,
  page-bottom-margin: 0.7in,
  page-left-margin: 0.7in,
  page-right-margin: 0.7in,
  page-show-footer: true,
  page-show-top-note: true,
  colors-body: rgb(0, 0, 0),
  colors-name: rgb(0, 79, 144),
  colors-headline: rgb(0, 79, 144),
  colors-connections: rgb(0, 79, 144),
  colors-section-titles: rgb(0, 79, 144),
  colors-links: rgb(0, 79, 144),
  colors-footer: rgb(128, 128, 128),
  colors-top-note: rgb(128, 128, 128),
  typography-line-spacing: 0.6em,
  typography-alignment: "justified",
  typography-date-and-location-column-alignment: right,
  typography-font-family-body: "Raleway",
  typography-font-family-name: "Raleway",
  typography-font-family-headline: "Raleway",
  typography-font-family-connections: "Raleway",
  typography-font-family-section-titles: "Raleway",
  typography-font-size-body: 10pt,
  typography-font-size-name: 30pt,
  typography-font-size-headline: 10pt,
  typography-font-size-connections: 10pt,
  typography-font-size-section-titles: 1.4em,
  typography-small-caps-name: false,
  typography-small-caps-headline: false,
  typography-small-caps-connections: false,
  typography-small-caps-section-titles: false,
  typography-bold-name: false,
  typography-bold-headline: false,
  typography-bold-connections: false,
  typography-bold-section-titles: false,
  links-underline: false,
  links-show-external-link-icon: false,
  header-alignment: left,
  header-photo-width: 3.5cm,
  header-space-below-name: 0.7cm,
  header-space-below-headline: 0.7cm,
  header-space-below-connections: 0.7cm,
  header-connections-hyperlink: true,
  header-connections-show-icons: true,
  header-connections-display-urls-instead-of-usernames: false,
  header-connections-separator: "",
  header-connections-space-between-connections: 0.5cm,
  section-titles-type: "with_full_line",
  section-titles-line-thickness: 0.5pt,
  section-titles-space-above: 0.5cm,
  section-titles-space-below: 0.3cm,
  sections-allow-page-break: true,
  sections-space-between-text-based-entries: 0.3em,
  sections-space-between-regular-entries: 1.2em,
  entries-date-and-location-width: 4.15cm,
  entries-side-space: 0.2cm,
  entries-space-between-columns: 0.1cm,
  entries-allow-page-break: false,
  entries-short-second-row: false,
  entries-degree-width: 1cm,
  entries-summary-space-left: 0cm,
  entries-summary-space-above: 0.12cm,
  entries-highlights-bullet:  "•" ,
  entries-highlights-nested-bullet:  "•" ,
  entries-highlights-space-left: 0cm,
  entries-highlights-space-above: 0.12cm,
  entries-highlights-space-between-items: 0.12cm,
  entries-highlights-space-between-bullet-and-text: 0.5em,
  date: datetime(
    year: 2026,
    month: 6,
    day: 19,
  ),
)


= Fani Bhushan

#connections(
  [#connection-with-icon("location-dot")[Berlin, Germany]],
  [#link("mailto:bhufani@gmail.com", icon: false, if-underline: false, if-color: false)[#connection-with-icon("envelope")[bhufani\@gmail.com]]],
  [#link("tel:+49-176-84733947", icon: false, if-underline: false, if-color: false)[#connection-with-icon("phone")[0176 84733947]]],
  [#link("https://linkedin.com/in/fani-bhushan", icon: false, if-underline: false, if-color: false)[#connection-with-icon("linkedin")[fani-bhushan]]],
)


== Professional Summary

Software engineer with 16 years of experience in technical leadership and software development, specializing in automotive infotainment and connected car services. Led the development of a Qt\/C++-based Online Media UI for MBUX and architected multi-platform connected car services for Mercedes-Benz. Seeking a leadership role to apply my expertise in technical leadership and cloud-native solutions to drive innovation.

== Experience

#regular-entry(
  [
    #strong[Expert Software Engineer], MBition GmbH -- Berlin, Germany

  ],
  [
    Mar 2018 – present

  ],
  main-column-second-row: [
    - Led the Dialog Engine integration (central embedded business logic component) for a high-priority LiquidAI NLU\/ASR model POC in the US market, which successfully green-lit the project and secured a 4.5 FTEs team budget.

    - Completed CSPO certification and served as Acting Product Owner for the Speech Assistant, leading PI planning, backlog management, capacity planning, and resolving critical blocker bug escalations.

    - Took ownership of a critical speech container service to implement an urgent feature, managing the end-to-end implementation, FOSS compliance, and market release.

    - Led the development of and implemented a Qt\/C++-based Online Media UI application for the MBUX Infotainment system on Linux, collaborating with geographically dispersed teams.

    - Contributing as an expert to the development of a Linux-based speech assistant using C++, Python, and Golang, leveraging Large Language Models (LLMs).

    - Deputy Product Owner, negotiating with stakeholders, coordinating across teams, and facilitating collaboration for multiple product lines.

    - Architected and led the development of Qt\/Golang\/Java-based multi-platform connected car services for Mercedes-Benz.

    - Resolved critical bug escalations and acted as Engineering Lead and Product Owner in their absence.

    - Mentored and coached engineering teams, driving best practices, scalability, and maintainability.

    - Led cross-functional collaboration with product managers, cloud backend teams, and UI developers to align technical roadmaps with business objectives.

    - Developed the Connected Services UI platform using Qt\/QML and C, integrated into a Linux-based UI package.

    - Developed multiple Qt\/C++-based connected car standalone and template apps, working closely with cloud backend and HU services teams.

  ],
)

#regular-entry(
  [
    #strong[Software Technical Lead], Wipro Technologies -- Bangalore, India \/ Tokyo, Japan \/ Germany

  ],
  [
    May 2010 – Jan 2018

  ],
  main-column-second-row: [
    - Handled line management responsibilities for the engineering team, including career mentorship, performance evaluations, and resource planning.

    - Led a team in the development of automotive infotainment projects using C++, including routing and route guidance components for the Navigation System.

    - Managed a team working on a C\#-based UI testing tool, incorporating Python and Perl scripting at Panasonic Automotive System Japan.

    - Worked on-site in Japan, collaborating with clients\/stakeholders while coordinating with offshore teams.

    - Defined engineering processes, quality standards, and best practices improving team efficiency and product reliability.

    - Worked on firmware development for a robotic vacuum cleaner using Embedded C and RTOS.

    - Developed firmware for a smart meter, utilizing Embedded C and RTOS.

    - Worked on-site in Germany, participating in test drives and handling product quality discussions with clients.

  ],
)

== Education

#education-entry(
  [
    #strong[Gandhi Institute of Engineering And Technology], Bachelors in Technology in Computer Science -- India

  ],
  [
    July 2005 – May 2009

  ],
  main-column-second-row: [
  ],
)

== Certifications

- Certified Scrum Product Owner (CSPO)

- Certified Professional for Software Architecture (iSAQB)

- Software Architecture Certification from Global Dev Experts

== Skills

#strong[Programming Languages:] C++, C\#, Golang, Java, Python, Perl, Embedded C

#strong[Frameworks \\& UI:] Qt\/QML, RTOS, Docker, Containers

#strong[Cloud \\& Microservices:] Microservices, Azure Cloud, gRPC

#strong[Domains:] Automotive Infotainment, Connected Car Services, Navigation Systems, Speech Assistants, LLMs (LiquidAI, ASR\/NLU)

#strong[Methodologies \\& Tools:] TDD, Automated Testing, GitLab CI, Azure DevOps, Agile, Scrum

== Languages

#strong[English:] Fluent

#strong[Hindi:] Fluent

#strong[German:] B1
