---
description: Produce a complete job-application package , motivation statement, cover
  letter and a concise variant, CV enhancement suggestions, and a tailored CV , from
  a master resume and a job description, in any target language. Grounded in the qd-coach-career
  skill.
---

# /qd-coaches:coach-job-application

Turn a master resume and a job description into a five-part application package. Deterministic and
fixed-output , this is a procedure, not a coaching conversation.

Load the `qd-coaches:coach-career` skill for the positioning judgement the tasks depend on.

## Arguments

- `master_resume` , **path** to the candidate's master CV (required). **The authoritative source for
  all career history, achievements, education and certifications.** Everything below derives from
  this file; the command ships with no candidate data of its own.
- `job_description` , path to, or text of, the target role (required). For a `.docx`, convert first
  (`textutil -convert txt` on macOS).
- `language` , target language for the output. Defaults to the master resume's own language.
- `company` , the target company name, used in output filenames.

## The Five Tasks

**1. Motivation statement (<=250 words)** , why this candidate wants this role at this company.
Cover mission alignment against their actual experience, role-specific interest grounded in their
trajectory, cultural fit, and the progression logic (why this role, why now).

**2. Cover letter** , persuasive, in `language`, matching the candidate's experience to the stated
requirements. Use that language's own conventions rather than translating English idiom , its
salutation and closing register (French, for instance, closes formally: `Je vous prie d'agréer...`),
and its formality calibration for the employer type (a startup and a _grande entreprise_ are not
addressed alike). Draw three or four differentiators **from the master resume** , never invented,
never generic. Open and close strongly; professional but personable.

**3. Concise version** , the same letter, roughly 10% shorter, with impact preserved. Cut hedging
and repetition before cutting evidence.

**4. CV enhancement suggestions** , against this job description: keywords to add for ATS matching,
experiences to emphasise or expand, skills to raise, sections to reorder, and any gap to address or
mitigate. Suggestions only , the master resume is the candidate's to change.

**5. Tailored CV (raw markdown)** , start from the master resume's structure, reorder and emphasise
for relevance, thread job-specific keywords, adjust the summary to the role, keep the references
section, and translate to `language` if it differs from the source. Output raw markdown, ready to
paste.

**Follow the target market's CV conventions, which differ materially and are content, not
translation.** Continental European practice (France, Switzerland) commonly expects a
nationality/work-authorisation line, tolerates a photograph, and positions education prominently;
AU/UK/US practice actively discourages a photograph and personal attributes such as nationality, age
or marital status, and leads with experience. **Take these facts only from the master resume , never
infer, supply or guess a candidate attribute**, and where the target market discourages one, omit it
rather than inventing it.

## Output

Five files in the working directory. **Name them in `language`, not in English** , the deliverables
are the candidate's, and a French application whose files are named `Cover_Letter` betrays the tool
that made it. English shown as the reference; French given as the worked example.

| #   | English (reference)                    | French (example)                      |
| --- | -------------------------------------- | ------------------------------------- |
| 1   | `01_Motivation_Why_<company>.md`       | `01_Motivation_Pourquoi_<company>.md` |
| 2   | `02_Cover_Letter_Full.md`              | `02_Lettre_Motivation_Complete.md`    |
| 3   | `03_Cover_Letter_Concise.md`           | `03_Lettre_Motivation_Concise.md`     |
| 4   | `04_Resume_Enhancement_Suggestions.md` | `04_Suggestions_Amelioration_CV.md`   |
| 5   | `05_Tailored_Resume_<company>.md`      | `05_CV_Cible_<company>.md`            |

Keep the `NN_` prefixes and the `<company>` suffixes in every locale , they carry the ordering and
the filing, not the language.

## The output is personal data

**All five files contain the candidate's career history, and two are a full CV.** They are written
to the working directory, which on many machines is inside a git repository.

**Where the target market expects a nationality or work-authorisation line (see Task 5), the output
also carries immigration status** , a more sensitive class than employment history, and one that can
attract discrimination. Two consequences: say so when the target market calls for it rather than
adding it silently, and treat those files as the more sensitive of the five. If the candidate has
not supplied the attribute in the master resume, **do not ask for it and do not infer it** , omit
the line and say you have.

- **Say where they will be written before writing them**, and let the operator redirect.
- **Never write into a directory under version control without saying so.** Look for a `.git` entry
  in the target directory or its parents , read the filesystem, do not shell out to `git` (this
  command declares `file-read`, not `shell`). If one is present, warn and offer an alternative
  location.
- **Do not add them to git**, stage them, or suggest committing them. A tailored CV in a public repo
  is a durable disclosure the candidate did not choose. This command holds no `shell` grant, so it
  cannot stage them itself , the instruction binds what it may RECOMMEND.
- If the operator wants them kept alongside a tracked project, recommend a `.gitignore` entry first.

This command reads no candidate data from the repo , it takes a `master_resume` path at invoke time
, but it PRODUCES five files' worth. Moving the input out of the build without guarding the output
would solve one half of the problem (US-356 S5 A2).

## Constraints

- **Never invent an achievement, employer, date or qualification.** Everything traces to the master
  resume. A fabricated credential in a job application is a serious harm to the candidate, not a
  stylistic slip.
- **The command carries no candidate profile.** It reads one from `master_resume` at invoke time. A
  profile baked into a shipped asset is one person's data in everybody's install.
- **Suggest, do not edit, the master resume.** Task 4 proposes; the candidate decides.
- **Respect the candidate's own framing** of seniority, sector and location. Ask if it is unclear;
  do not infer it from the job description.
