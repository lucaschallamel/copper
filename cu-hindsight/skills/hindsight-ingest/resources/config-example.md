# Example `.hindsight-ingest.json`

Every key the tool accepts. Only `bank` and `forbidden` are required; an unknown key is an error.
Copy the block into `<vault>/.hindsight-ingest.json` and adapt it.

```json
{
  "bank": "vault-notes",
  "forbidden": ["Private", "Finance/Statements"],
  "exclude_dirs": ["/_INBOX", "/_ARCHIVES"],
  "exclude_files": ["AGENTS.md", "CLAUDE.md"],
  "pilot": ["Journal"],
  "detectors": ["fr-nir", "iban"],
  "tags": ["vault:notes"],
  "sync_host": "my-laptop",
  "allow_insecure_transport": false,
  "include_drawings": false,
  "batch_size": 5,
  "pause_s": 20,
  "timeout_s": 300,
  "max_chars": 200000,
  "max_delete_ratio": 0.1
}
```

| Key                                  | Default    | Meaning                                                                                                                                             |
| ------------------------------------ | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bank`                               | (required) | The Hindsight bank this vault fills; must already exist (`init-bank`)                                                                               |
| `forbidden`                          | (required) | Folders never listed, read, scanned or sent; a name matches at any depth, a path with `/` (or a leading `/`, as `/_INBOX`) only from the vault root |
| `exclude_dirs`                       | `[]`       | Folders skipped like `forbidden` (transit, archive)                                                                                                 |
| `exclude_files`                      | `[]`       | File names never sent, in every folder including the vault root                                                                                     |
| `pilot`                              | `[]`       | Folders sent by `send pilot`                                                                                                                        |
| `detectors`                          | `[]`       | Opt-in masks: `fr-nir`, `iban` (password lines are always redacted)                                                                                 |
| `tags`                               | `[]`       | Extra tags on every document                                                                                                                        |
| `sync_host`                          | none       | The only host allowed to run `sync`                                                                                                                 |
| `allow_insecure_transport`           | `false`    | Allow plain `http://` to a tailnet address                                                                                                          |
| `include_drawings`                   | `false`    | Send Excalidraw drawings (`*.excalidraw.md`); they are mostly drawing data                                                                          |
| `batch_size`, `pause_s`, `timeout_s` | 5, 20, 300 | Throttle and per-request timeout                                                                                                                    |
| `max_chars`                          | 200000     | Notes above this are skipped                                                                                                                        |
| `max_delete_ratio`                   | 0.1        | Above this share of missing notes, `sync` deletes nothing                                                                                           |
