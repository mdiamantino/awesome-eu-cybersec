# Verification notes

Final entries: **89**. Every included URL was fetched and its page or document was checked against the claimed resource. A large-batch timeout affected several URLs; six were confirmed in a smaller follow-up fetch, and five hardware-security repositories were verified in a separate gap pass. Entries blocked by robots rules were discarded rather than inferred from search results.

## Counts by category and subcategory

| Category | Subcategory | Count |
|---|---|---:|
| Governance, Risk & Policy Mapping | NIS2 | 3 |
| Governance, Risk & Policy Mapping | GDPR and PETs | 1 |
| Governance, Risk & Policy Mapping | EU AI Act | 2 |
| Financial Sector Resilience (DORA) | ICT Third-Party Risk Registers | 2 |
| Financial Sector Resilience (DORA) | Threat-Led Penetration Testing | 2 |
| Financial Sector Resilience (DORA) | Incident Classification and Reporting | 2 |
| Software Supply Chain & Product Security (CRA) | CRA Implementation Guidance | 2 |
| Software Supply Chain & Product Security (CRA) | Conformity Assessment | 2 |
| Software Supply Chain & Product Security (CRA) | Open Source and SBOM | 1 |
| Sovereign Identity & Trust (eIDAS) | Signature and Trust-Service Tooling | 2 |
| Sovereign Identity & Trust (eIDAS) | EUDI Wallet Implementations and Testing | 2 |
| Sovereign Identity & Trust (eIDAS) | eIDAS Technical Standards | 3 |
| Sovereign Cloud & DevSecOps | Gaia-X Specifications & Architecture | 3 |
| Sovereign Cloud & DevSecOps | National Sovereign Cloud Certification & Qualification Schemes | 4 |
| Sovereign Cloud & DevSecOps | EU-Hosted DevSecOps Tooling | 1 |
| Cyber-Physical Security | Energy & Industrial Control Systems (OT/ICS/SCADA) | 3 |
| Cyber-Physical Security | Transport & Automotive | 2 |
| Cyber-Physical Security | Maritime & Port Security | 2 |
| Cyber-Physical Security | Aerospace & Space Telemetry | 4 |
| Cyber-Physical Security | Hardware & Embedded Security Auditing | 5 |
| Telecom, 5G & Network Infrastructure Security | 5G/Mobile Network Security | 5 |
| Telecom, 5G & Network Infrastructure Security | Open RAN Security | 1 |
| Telecom, 5G & Network Infrastructure Security | Fixed & Submarine Cable Infrastructure Security | 4 |
| Threat Intelligence | EU and National Threat Intelligence | 6 |
| Training & Cyber Ranges | Cyber Range Platforms | 4 |
| Training & Cyber Ranges | Competitions & CTF Infrastructure | 1 |
| Training & Cyber Ranges | Skills & Competency Frameworks | 3 |
| Training & Cyber Ranges | Awareness & Workforce Training Resources | 5 |
| National Cybersecurity Authorities & Standards | France/ANSSI | 2 |
| National Cybersecurity Authorities & Standards | Germany/BSI | 2 |
| National Cybersecurity Authorities & Standards | Netherlands/NCSC-NL | 1 |
| National Cybersecurity Authorities & Standards | United Kingdom/NCSC | 2 |
| National Cybersecurity Authorities & Standards | Finland/NCSC-FI | 1 |
| National Cybersecurity Authorities & Standards | EU/CERT-EU | 1 |
| National Cybersecurity Authorities & Standards | EU/ENISA | 1 |
| National Cybersecurity Authorities & Standards | Ireland/NCSC | 2 |

## Discarded during URL verification

- **Website Evidence Collector** — fetch failed or was blocked (`crawler error bad_robots_code: bad_robots_code`).
- **EDPS Inspection Software** — fetch failed or was blocked (`crawler error bad_robots_code: bad_robots_code`).
- **EUDI Wallet Developer Documentation** — fetch failed or was blocked (`crawler error http_code_client_error: http_code_client_error`).
- **Gaia-X GitLab** — fetch failed or was blocked (`crawler error broken_content_ip_block: broken_content_ip_block`).
- **UN Regulation No. 155** — fetch failed or was blocked (`crawler error disallow_by_robots: disallow_by_robots`).
- **UN Regulation No. 156** — fetch failed or was blocked (`crawler error disallow_by_robots: disallow_by_robots`).
- **KU Leuven COSIC Security Evaluations Lab** — fetch failed or was blocked (fetch timed out).
- **TOFU Fault-Injection Method** — fetch failed or was blocked (fetch timed out).
- **Portuguese Cybersecurity Competencies Framework** — fetch failed or was blocked (`crawler error bad_robots_code: bad_robots_code`).
- **CCN-STIC 817 Cyber-Incident Management** — fetch failed or was blocked (`crawler error bad_robots_code: bad_robots_code`).
- **Belgian CyberFundamentals Framework** — fetch failed or was blocked (`crawler error bad_robots_code: bad_robots_code`).
- **Belgian NIS2 Quickstart Guide** — fetch failed or was blocked (`crawler error bad_robots_code: bad_robots_code`).
- **FISSA** and **Proxmark3 Iceman Fork** — resolved in a follow-up fetch but were omitted because the fetched pages did not establish sufficiently direct European public-body or university maintenance.

## Critic pass

The critic pass checked No-Pitch, direct EU relevance, resource/title matching, and FOSS-first treatment. Entries with only an over-specific title or description were corrected and retained; entries with a substantive mismatch or insufficient evidence were removed.

### Corrected after critic flag

- **NIS2 Public Control Framework** — corrected title/description; final name: **nis2-public**.
- **eIDAS Standards and Specifications** — corrected title/description; final name: **eIDAS Standards and Specifications**.
- **ENISA Overview of Standards Related to eIDAS** — corrected title/description; final name: **ENISA Overview of Standards Related to eIDAS**.
- **Gaia-X Trust Framework Architecture** — corrected title/description; final name: **Gaia-X Trust Framework Architecture**.
- **SecNumCloud** — corrected title/description; final name: **SecNumCloud**.
- **EUCS Candidate Cloud Certification Scheme** — corrected title/description; final name: **EUCS Candidate Cloud Certification Scheme**.
- **European Commission Cloud Sovereignty Framework** — corrected title/description; final name: **European Commission Cloud Sovereignty Framework**.
- **BSI TR-03163 Security in 5G Networks** — corrected title/description; final name: **BSI TR-03163 Security in Telecommunications Infrastructure**.
- **EU Recommendation on Submarine Cable Security** — corrected title/description; final name: **EU Recommendation on Submarine Cable Security**.
- **EU Submarine Cable Security Toolbox** — corrected title/description; final name: **EU Submarine Cable Security Toolbox**.
- **ENISA Undersea Cables Report** — corrected title/description; final name: **ENISA Undersea Cables**.
- **EU Report on Submarine Cable Resilience** — corrected title/description; final name: **EU Report on Submarine Cable Resilience**.
- **European Vulnerability Database** — corrected title/description; final name: **European Vulnerability Database**.
- **NCSC-NL Security Advisories CSAF Feed** — corrected title/description; final name: **NCSC-NL Security Advisories CSAF Feed**.
- **ENISA SME Training Material** — corrected title/description; final name: **ENISA SME Training Material**.
- **UK NCSC Cyber Assessment Framework** — corrected title/description; final name: **UK NCSC Cyber Assessment Framework**.

### Removed after critic flag

- **Gaia-X Architecture Document** — Reject: The fetched excerpt matches the Gaia-X architecture page, but it explicitly states that EU or European national relevance is not stated. It therefore does not prove the required specific European technical-scheme or institutional relevance. The description also overstates the excerpt by calling the infrastructure European and asserting that it defines components and a trust model, while the excerpt only describes Gaia-X trust-related architecture and specifications. No direct mismatch in resource identity, but the entry fails the strict relevance and description-support requirements.
- **Esquema Nacional de Seguridad Certification** — Reject: the verification excerpt matches the ENS certification page title but only confirms a list of entities certified under ENS. It does not establish EU/EU-law relevance, identify an official Spanish government or European issuing body, or provide evidence supporting the description's claim about assessing systems and cloud services. Open-source status is also not stated.
- **LARS ICS** — Reject: the excerpt does not explicitly establish EU-level or European national relevance, identify BSI as the issuing organization, or confirm an open-source license. It only states that complete source code is included. The description also overstates the evidence by attributing the tool to BSI and characterizing it specifically as supporting German industrial control environments.
- **Danish Port Cybersecurity Guidance** — The URL is hosted by the Danish Transport Authority and the submitted name/description identify a Danish authority guidance document, but the verification excerpt identifies a different resource: “Guidance on how to treat cybersecurity at the port facility and port level,” SAGMAS doc. 6903, issued by the European Commission. This is a material identity and issuer mismatch, so the entry should be rejected or re-verified against the linked PDF.
- **OCCTET Toolkit** — The verification excerpt matches the OCCTET resource and confirms an EU-funded, open-source toolkit focused on EU Cyber Resilience Act compliance for FOSS. However, it does not support the submitted description's claims about port operational technology or training; the entry appears to conflate OCCTET with another resource.
- **ENISA Security in Open RAN** — Flagged mismatch: the URL is hosted on ENISA’s site, but the fetched excerpt identifies the resource as a PwC/PricewaterhouseCoopers presentation rather than an ENISA-issued resource. It also explicitly says it is not a standard, framework, guidance document, threat-intelligence feed, or tool, so the description overstates ENISA’s role and the resource’s status. Although the presentation mentions EU member states, ENISA, German BSI, and European deployments, this does not cure the issuer mismatch.
- **ECSC Gameboard** — The excerpt matches the ECSC Gameboard and establishes European relevance through the European Cyber Security Challenge, but it does not explicitly verify that the repository is open source or identify the license type. The description's claims that it is "ENISA's" and "open-source" therefore overstate what the excerpt proves. The entry should not be retained without stronger verification or a more cautious description.
- **ECSC 2024 Jeopardy Challenges** — Reject: the resource matches the named repository and has credible public GPL-3.0 open-source status, but the excerpt only establishes that it is a set of CTF challenges held in Turin for ECSC 2024 and explicitly does not prove specific EU, official European government/agency/university, or European technical-scheme relevance. It is also a challenge repository rather than a cybersecurity tool, so the entry type is questionable.
- **openECSC 2024 Challenges** — The repository and European relevance are verified, and it is publicly available under GPL-3.0. However, the entry is classified as a “Tool,” while the excerpt explicitly says it is not a cybersecurity tool but a collection of CTF challenge source code and related resources. Reclassify it as training/CTF content rather than a tool.
- **NCSC-NL Basisscan Cyberweerbaarheid** — Reject: the verification excerpt matches the Basisscan and describes its 25-statement assessment and report, but it does not explicitly establish an official European government/agency issuer, EU relevance, open-source status, or justified sovereign infrastructure. The NCSC-NL domain and metadata are insufficient under the strict evidence requirement.
- **ENS National Security Framework** — Reject. The excerpt confirms that ENS is a CCN framework and describes its compliance process, so the official Spanish-government relevance is supported. However, the fetched resource is a broad “ENS - Home” page rather than a clearly implementation-focused framework document, and the description overstates the excerpt by claiming that ENS establishes specific security principles and controls, which are not stated in the verification text. No open-source status is relevant because this is a framework, not a tool.
- **ENISA National Capabilities Assessment Framework 2.0** — Reject: the fetched excerpt identifies the resource as the “National Cybersecurity Assessment Framework (NCAF) Tool,” not “ENISA National Capabilities Assessment Framework 2.0,” creating a title/resource mismatch. The excerpt also does not substantiate the claim that it provides a method specifically for EU member states, and it does not establish open-source status. Although ENISA and the enisa.europa.eu domain suggest an EU connection, the excerpt expressly states that no further explicit EU or European-national relevance is provided.

## Coverage note

The requested target of 5–10 entries was not padded where fewer official or clearly open resources could be verified. Sparse subsections therefore contain only the resources that passed URL and critic checks.
