---
title: BANZA_MESSAGING_REWRITE_MAP
version: 1.0
date: 2026-05-30
status: AUDIT COMPLETE — no modifications applied
---

# BANZA Messaging Rewrite Map

**Purpose:** Working document for the execution phase. Every key message across every surface, mapped as CURRENT → IMPLICIT → DESIRED.

**Format:** Each entry identifies the surface, location, the current text, what it implies to a visitor, and the desired message. Entries are ordered by priority (P0/P1/P2) and grouped by surface.

**Rule:** DESIRED messages are proposals, not final copy. Tone, length, and exact wording will be refined during execution. The strategic content of DESIRED is what is canonical.

---

## Priority Key

- **P0** — Absence of this message makes the canonical thesis invisible
- **P1** — Absence of this message weakens differentiation
- **P2** — Absence of this message leaves supporting narrative incomplete

---

## Surface: Homepage (`/`)

---

### MSG-HP-001 (P0) — Problem Section Frame

**Location:** `app/page.tsx` — above the problem card grid, before the grid `<div>`

```
CURRENT:  [No framing sentence above the problem cards]

IMPLICIT: Five independent product problems solved by one payment app (Banzami)

DESIRED:
Eyebrow: "A raiz do problema"
H2: "Angola tem as peças. Falta a camada de protocolo."
Body: "Angola tem carris de liquidação (EMIS), transferências bancárias e
       aplicações de pagamento. O que Angola não tem é uma camada aberta
       entre eles: regras certificadas que qualquer programador, operador ou
       instituição pode adoptar sem negociar acesso a uma rede fechada.
       BANZA é essa camada. Os problemas abaixo são sintomas da sua ausência."
```

---

### MSG-HP-002 (P0) — Problem Card Set

**Location:** `app/page.tsx` — `problems` array

```
CURRENT:
  { icon: '💵', title: 'Dependência de dinheiro físico',
    desc: 'Comerciantes perdem vendas por falta de troco...' }
  { icon: '📸', title: 'Comprovativos por WhatsApp',
    desc: 'Pagamentos manuais que exigem captura de ecrã...' }
  { icon: '📱', title: 'Apps sem pagamento integrado',
    desc: 'Táxis, delivery e ecommerce angolanos não têm gateway...' }
  { icon: '🏪', title: 'Pequenos negócios excluídos',
    desc: 'TPA físico é caro e burocrático...' }
  { icon: '🔧', title: 'Sem SDK angolano',
    desc: 'Programadores angolanos não têm uma API de pagamentos...' }

IMPLICIT: Five separate product problems, each solvable by a product feature

DESIRED:
  Each card retains its content, but the card group should be preceded
  by MSG-HP-001 (the structural framing). Optionally, the TPA card is
  updated to name the structural reason:

  { icon: '🏪', title: 'Pequenos negócios excluídos',
    desc: 'O TPA requer contratos de acquiring, hardware e relações bancárias
           que a maioria das pequenas empresas não consegue obter. Um QR
           impresso chega. Sem acquiring. Sem hardware. Sem gatekeeping.' }

  The "Sem SDK angolano" card updated:

  { icon: '🔧', title: 'Sem protocolo angolano',
    desc: 'Programadores angolanos não têm uma API de pagamentos nativa —
           nem um protocolo aberto que qualquer app possa implementar sem
           negociar acesso institucional.' }
```

---

### MSG-HP-003 (P0) — Wallet Section

**Location:** `app/page.tsx` — wallet section eyebrow + H2

```
CURRENT:
  Eyebrow: "Filosofia wallet-native"
  H2: "O telemóvel é a carteira."

IMPLICIT: BANZA is a mobile wallet product

DESIRED:
  Eyebrow: "Filosofia wallet-native"
  H2: "Wallet-native é uma propriedade do protocolo, não de uma app."
  Body sub-text update: "Qualquer operador certificado no BANZA é
  wallet-native por design — não porque é uma funcionalidade do Banzami,
  mas porque o protocolo define carteiras como a primitiva de pagamento."
```

---

### MSG-HP-004 (P1) — QR Section

**Location:** `app/page.tsx` — QR section eyebrow + H2 + body

```
CURRENT:
  Eyebrow: "QR Commerce"
  H2: "QR como primitiva nativa do protocolo."
  Body: "Do táxi à escola, da cantina à plataforma de doações — qualquer
         operador Banza pode emitir e aceitar pagamentos QR."

IMPLICIT: BANZA is a QR payment system (even though H2 says "protocolo",
          the eyebrow "QR Commerce" leads)

DESIRED:
  The H2 already contains the right claim ("primitiva nativa do protocolo").
  Update the body to reinforce protocol-level framing:
  "Qualquer operador certificado no BANZA emite e aceita QR — sem hardware
   dedicado, sem acquiring, sem intermediários. QR é uma primitiva do
   protocolo: não uma funcionalidade de produto que pode ser removida."
```

---

### MSG-HP-005 (P0) — Closing ManifestoQuote

**Location:** `app/page.tsx` — second ManifestoQuote (before reference grid)

```
CURRENT:
  "O QR torna-se o terminal. O telemóvel torna-se a carteira.
   Angola salta directamente para a infraestrutura de pagamento do futuro."

IMPLICIT: This is a QR + mobile product vision

DESIRED:
  "O que torna o salto possível não é um produto. É a camada de protocolo
   que qualquer operador, programador e instituição pode adoptar. BANZA
   é essa camada."

  (or, shorter):
  "O protocolo é o que torna o salto possível. O QR, a carteira e o SDK
   são o que acontece quando qualquer operador pode construir sobre ele."
```

---

### MSG-HP-006 (P1) — SDK Section

**Location:** `app/page.tsx` — developer section eyebrow + body

```
CURRENT:
  Eyebrow: "Para programadores"
  H2: "SDK-first. Integração em Kwanza."
  Body: "O Banza é SDK-first. Qualquer app — táxi, delivery, escola,
         ecommerce — integra pagamentos em Kwanza com uma única chamada
         ao Banzami SDK oficial."

IMPLICIT: "SDK-first" is a product feature; calling the SDK is calling Banzami

DESIRED:
  H2: "SDK-first. Integração em Kwanza. Sem acesso institucional."
  Body: "Nenhum gateway internacional suporta AOA nativamente. A integração
         directa com EMIS exige relações institucionais indisponíveis a startups.
         O BANZA é a camada aberta: qualquer programador integra em horas,
         sem contrato bancário, com liquidação T+0 garantida pelo protocolo."
```

---

### MSG-HP-007 (P2) — Ecosystem Section

**Location:** `app/page.tsx` — ecosystem section body

```
CURRENT:
  Eyebrow: "Ecossistema"
  H2: "Uma rede. Múltiplos actores."
  Body: "Consumidores, comerciantes, apps externas, Banzami SDKs, bancos e
         o core financeiro — todos ligados através de uma infraestrutura do Banza."

IMPLICIT: BANZA is the central hub connecting everyone (hub-and-spoke product model)

DESIRED:
  H2: "Uma rede. Múltiplos operadores."
  Body: "Qualquer entidade certificada pode operar no protocolo BANZA —
         bancos, fintechs, apps e programadores independentes.
         O protocolo define as regras. Os operadores constroem os produtos.
         Os utilizadores escolhem onde querem estar."
```

---

### MSG-HP-008 (P1) — EcosystemMap center node

**Location:** `components/EcosystemMap.tsx` — center SVG node

```
CURRENT:
  Center node text: "BANZA" / "API · Ledger · Core Rust"

IMPLICIT: BANZA is a central API/backend (technology-level description)

DESIRED:
  Center node text: "BANZA" / "protocolo · regras · certificação"

  (This changes what BANZA "is" in the diagram: from a technology stack
   to a protocol standard — which is what connects all the outer actors.)
```

---

## Surface: Reference §1 (`/o-que-e-o-banza`)

---

### MSG-REF-001 (P0) — Opening negative definitions

**Location:** `docs/BANZAMI_REFERENCE.md`, line 42

```
CURRENT:
  "Não é um banco. Não é uma carteira digital simples. Não é uma plataforma
   fintech genérica adaptada de um modelo ocidental. É o protocolo que
   define como o dinheiro se move digitalmente em Angola — com regras
   imutáveis, invariantes financeiros verificáveis e uma camada de
   inteligência artificial que explica cada decisão do protocolo."

IMPLICIT: BANZA is defined by what it is not, with a protocol description
           appended. Does not explain WHY the protocol is necessary.

DESIRED:
  "Não é um banco. Não é uma carteira digital simples. Não é uma plataforma
   fintech genérica adaptada de um modelo ocidental.

   Existe porque nenhuma destas coisas fornece o que Angola precisa: uma
   camada de protocolo aberta — regras verificáveis que qualquer programador,
   operador ou instituição pode adoptar sem negociar acesso a uma rede fechada.

   É o protocolo que define como o dinheiro se move digitalmente em Angola
   — com operadores certificados, invariantes financeiros verificáveis e um
   sistema operativo nativo capaz de explicar, validar e evoluir o protocolo."
```

---

### MSG-REF-002 (P1) — Blockchain disambiguation

**Location:** `docs/BANZAMI_REFERENCE.md`, after line 42 — new paragraph

```
CURRENT:  [Absent]

IMPLICIT: Unclear — BANZA's protocol language ("invariants," "federation,"
           "immutable ledger") resembles blockchain terminology.

DESIRED:
  "O BANZA não é blockchain. Não há tokens, não há cadeia distribuída,
   não há criptomoeda. O ledger do BANZA é um sistema Rust determinístico —
   liquidação atómica, registos imutáveis, sempre em Kwanza, integrado
   nos carris EMIS de Angola."
```

---

### MSG-REF-003 (P0) — "O protocolo é o produto" principle

**Location:** `docs/BANZAMI_REFERENCE.md`, §2 Princípios Fundamentais

```
CURRENT:
  ### O protocolo é o produto
  O Banzami (o produto de consumo) é a implementação de referência do
  protocolo Banza. O protocolo é o que escala. O Banzami é o que prova
  que funciona.

IMPLICIT: "This is one of six design principles" — no visual prominence

DESIRED:
  The principle heading remains. Add a callout block after the paragraph:

  > **O que isto significa:** Banzami é para o BANZA o que o Google Pay
  > é para o UPI — o maior produto numa rede que qualquer operador
  > certificado pode integrar. O protocolo não pertence ao Banzami.
  > O Banzami pertence ao protocolo.
```

---

### MSG-REF-004 (P0) — §15 Pix/UPI/M-Pesa comparison

**Location:** `docs/BANZAMI_REFERENCE.md`, §15 ("A oportunidade" subsection)

```
CURRENT:
  "O modelo está provado: o Pix no Brasil, o UPI na Índia, o M-Pesa em
   Moçambique. Angola tem as mesmas pré-condições. O Banza é a infraestrutura."

IMPLICIT: BANZA is similar to Pix, UPI, and M-Pesa

DESIRED:
  "O modelo está provado — mas a distinção importa.

   O Pix unificou os pagamentos digitais do Brasil porque é um protocolo
   aberto: qualquer banco, fintech ou operador que passe a certificação
   pode implementá-lo. Não é propriedade de nenhuma empresa. A interoperabilidade
   está nas regras, não nos contratos bilaterais. O UPI fez o mesmo para
   a Índia — o PhonePe, o Google Pay e o Paytm são todos operadores no mesmo
   protocolo aberto, governado pelo NPCI.

   O M-Pesa é diferente. O M-Pesa é uma rede fechada: a Safaricom define
   as regras, controla o acesso e nenhuma empresa independente pode
   'implementar o M-Pesa'. Quando a Safaricom muda os preços, todos os
   utilizadores e comerciantes estão sujeitos a essa decisão.

   O BANZA segue o modelo Pix/UPI, não o modelo M-Pesa. É um protocolo
   aberto com certificação pública. O Banzami é o primeiro operador —
   equivalente ao que o Itaú é ao Pix ou ao PhonePe é ao UPI. O protocolo
   não pertence ao Banzami. Angola tem as mesmas pré-condições que o Brasil
   e a Índia tinham. O Banza é a infraestrutura."
```

---

## Surface: Operators (`/operators`)

---

### MSG-OPS-001 (P0) — Hero body

**Location:** `app/operators/page.tsx` — hero body paragraph

```
CURRENT:
  "Registo curado de operadores que implementam o protocolo Banza.
   Manifests validados, capacidades declaradas, níveis de conformidade
   e preparação para federação — visibilidade de infraestrutura, não
   exposição de dados financeiros."

IMPLICIT: "Here is a list of companies using Banza"

DESIRED:
  "O BANZA é um protocolo aberto: qualquer entidade que passe o conformance
   suite torna-se operador certificado — sem negociar acesso a uma rede
   fechada. Este registo mostra quem já certificou. Quando a federação
   estiver activa, qualquer operador abaixo poderá interoperar com todos
   os outros — sem acordos bilaterais adicionais."
```

---

### MSG-OPS-002 (P1) — Footer conformance note

**Location:** `app/operators/page.tsx` — footer third item

```
CURRENT:
  "Os níveis de conformidade (0–4) são determinados pelo runner oficial
   do Banza. Nenhum operador pode auto-declarar certificação sem ter
   passado os testes."

IMPLICIT: Quality assurance mechanism for Banza's partners

DESIRED:
  "Os níveis de conformidade são determinados pelo conformance suite
   oficial — aplicado igualmente a todos os operadores, incluindo o
   Banzami. Nenhuma entidade declara certificação que não tenha verificado.
   Isto é o que distingue um protocolo aberto de uma rede fechada: as
   regras aplicam-se a todos os participantes sem excepção."
```

---

### MSG-OPS-003 (P0) — Missing ecosystem argument

**Location:** `app/operators/page.tsx` — new block needed before operator grid

```
CURRENT:  [Absent — no explanation of WHY the operator model matters]

IMPLICIT: This is a partner directory

DESIRED:
  New block above the filter/grid:

  "Porque é que os operadores importam

   Em redes fechadas, quem controla a rede decide quem pode participar.
   No BANZA, o protocolo é aberto: as regras são públicas, a certificação
   é verificável, e qualquer entidade qualificada pode entrar.

   Cada operador certificado é prova de que o protocolo funciona
   independentemente do Banzami. Quando a federação estiver activa,
   cada operador interopera automaticamente com todos os outros."
```

---

## Surface: Validation (`/validacao`)

---

### MSG-VAL-001 (P1) — Hero body

**Location:** `app/validacao/page.tsx` — hero body paragraph

```
CURRENT:
  "Acompanhamento rigoroso da implementação das funcionalidades descritas
   em BANZAMI_REFERENCE.md. Cada item rastreado ao documento de referência oficial."

IMPLICIT: This is a development tracker made visible

DESIRED:
  "O BANZA publica o estado de implementação publicamente porque o protocolo
   é aberto — as suas regras, o seu progresso e os seus invariantes são
   visíveis a operadores, programadores e reguladores. Nenhum outro sistema
   de pagamento em Angola publica este nível de detalhe. Isto é o que
   transparência de protocolo significa — não uma caixa negra."
```

---

### MSG-VAL-002 (P1) — Governance notice

**Location:** `app/validacao/page.tsx` — governance notice

```
CURRENT:
  "Consulta pública · edição restrita à administração Banzami"

IMPLICIT: "You can view, but not edit"

DESIRED:
  "Público por desenho — o protocolo BANZA é aberto; a sua execução também.
   Consulta pública · edição restrita à administração Banzami."
```

---

## Surface: Roadmap (`/roadmap`)

---

### MSG-RM-001 (P0) — Page scope

**Location:** `app/roadmap/page.tsx` — page structure

```
CURRENT:
  28 BanzAI roadmap items. Zero BANZA protocol milestones.

IMPLICIT: BANZA's future is BanzAI tooling

DESIRED:
  Two tracks:

  Track 1 — "BanzAI Protocol OS" (current content, relabelled)
  Track 2 — "BANZA Protocol" (new section with milestones from §16
              of the reference):

  H2: "BANZA Protocol Roadmap"
  Items:
  - Conformance Suite v1 (H2 2026) — testes executáveis para Níveis 1–3
  - Certificação Nível 1–2 (H2 2026) — primeiros operadores externos
  - Certificação Nível 3–4 (H1 2027) — protocolo completo
  - RFC de federação (H1 2027) — especificação de interoperabilidade
  - Operadores de terceiros (H1 2027) — primeiros não-Banzami no protocolo
  - Piloto de federação (H2 2027) — dois operadores em federação controlada
  - Federação aberta (2028) — qualquer operador Nível 4
  - Carris cross-border (2028+) — AOA ↔ outras moedas africanas
```

---

### MSG-RM-002 (P1) — Opening body

**Location:** `app/roadmap/page.tsx` — description paragraph

```
CURRENT:
  "Roadmap público do BanzAI — Protocol Operating System for the Banza protocol.
   We publish this transparently because trust begins with visibility."

IMPLICIT: Transparency is a BanzAI value

DESIRED:
  "Transparência é um valor do protocolo BANZA — não apenas do BanzAI.
   Este roadmap cobre dois tracks: o BanzAI Protocol OS (o sistema operativo
   cognitivo do protocolo) e o protocolo BANZA (federação, operadores abertos,
   certificação e ecossistema). Ambos são públicos porque o protocolo é aberto."
```

---

## Surface: BanzAI Interface (`/banzamia`)

---

### MSG-BIA-001 (P0) — No landing state

**Location:** `app/banzamia/page.tsx` — before BanzamIAApp renders

```
CURRENT:
  Full-screen interface loads immediately. Zero framing.

IMPLICIT: BanzAI is a chatbot. A payment chatbot.

DESIRED:
  Option A — Landing state (2-3 seconds before interface opens):
  Title: "BanzAI"
  Label: "Protocol Operating System"
  Line 1: "O protocolo explica-se a si mesmo."
  Line 2: "Ferramentas determinam a verdade. A IA explica a verdade."
  Capabilities: [Compreender] [Explicar] [Validar] [Simular] [Certificar] [Federar]
  CTA: "Abrir interface →"

  Option B — Persistent banner in interface:
  One-line header: "BanzAI — Protocol Operating System · Não é um chatbot.
  É a interface cognitiva do protocolo. [Sobre o BanzAI →]"
```

---

### MSG-BIA-002 (P1) — Chat input placeholder

**Location:** `components/banzamia/HomeBanzamIAEntry.tsx` and the full interface

```
CURRENT:
  Placeholder: "Pergunte sobre QR, SDKs, operadores, certificação, invariantes…"

IMPLICIT: "This is a support chatbot for Banza products"

DESIRED:
  "Pergunte sobre o protocolo: RFCs, invariantes, certificação, federação,
   integração, arquitectura..."

  (Removing "QR" and "SDKs" as the first examples moves away from product
   support framing toward protocol OS framing.)
```

---

### MSG-BIA-003 (P2) — Missing link to /sobre-banzamia

**Location:** BanzAI interface header or sidebar

```
CURRENT:
  No link to /sobre-banzamia from the interface

IMPLICIT: There is no explanation — the interface is self-contained

DESIRED:
  "Sobre o BanzAI →" link in the interface header, sidebar top, or as a
   persistent chip below the module tabs.
```

---

## Surface: Programadores (`/banzami-para-programadores`)

---

### MSG-DEV-001 (P0) — Opening line

**Location:** `docs/BANZAMI_REFERENCE.md`, §10 opening

```
CURRENT:
  "Integração em horas — A superfície de integração oficial do Banza são os SDKs.
   Integrações directas via HTTP não são o caminho recomendado."

IMPLICIT: "Here is how to use the SDK" — assumes the developer has already decided

DESIRED:
  New paragraph before the SDK table:

  "Nenhum gateway internacional suporta AOA (Kwanza) nativamente. A integração
   directa com EMIS exige relações institucionais fora do alcance de startups.
   Construir de raiz significa reconstruir as garantias que o protocolo já impõe.

   O BANZA é a camada aberta: certificado, Kwanza-nativo, QR-first, liquidação
   T+0 garantida por invariante de protocolo — não por política de empresa.
   Qualquer programador integra sem contrato bancário, sem acquiring, sem acesso
   institucional.

   A superfície de integração oficial são os SDKs:"
```

---

### MSG-DEV-002 (P1) — SDK table framing

**Location:** `docs/BANZAMI_REFERENCE.md`, §10 SDK table

```
CURRENT:
  | SDK | Pacote | Casos de uso |
  (table with TypeScript, Flutter, PHP — no protocol context)

IMPLICIT: "These are Banzami's product SDKs"

DESIRED:
  Add a note above or below the table:
  "Estes SDKs implementam o protocolo BANZA. Uma app que os integra
   torna-se parte do ecossistema de operadores certificados — não apenas
   um cliente do Banzami."
```

---

## Surface: Comerciantes (`/banzami-para-comerciantes`)

---

### MSG-MER-001 (P1) — T+0 settlement attribution

**Location:** `docs/BANZAMI_REFERENCE.md`, §11 T+0 section

```
CURRENT:
  "O montante líquido é creditado na carteira do comerciante imediatamente
   após a confirmação do pagamento. Não há espera de dias bancários."

IMPLICIT: "This is a Banzami product feature — our policy is T+0 settlement"

DESIRED:
  "O montante líquido é creditado imediatamente após a confirmação —
   não há espera de dias bancários. A liquidação T+0 é um invariante do
   protocolo BANZA (INV-STL-001): todos os operadores certificados são
   obrigados a cumpri-la. Não é uma política do Banzami — é uma garantia
   do protocolo."
```

---

### MSG-MER-002 (P2) — Section opener

**Location:** `docs/BANZAMI_REFERENCE.md`, §11 opening

```
CURRENT:
  [Section opens immediately on "Sem hardware. Sem burocracia."]

IMPLICIT: This is entirely a Banzami product section

DESIRED:
  One opening sentence:
  "O Banzami é construído sobre o protocolo BANZA — e as garantias
   que um comerciante recebe (sem TPA, T+0, sem acquiring) derivam
   do protocolo, não apenas do produto."

  Then: "Sem hardware. Sem burocracia." (existing content)
```

---

## Surface: Architecture (`/arquitectura-tecnica`)

---

### MSG-ARC-001 (P1) — No strategic frame

**Location:** `docs/BANZAMI_REFERENCE.md`, §4 opening

```
CURRENT:
  [Sections opens immediately on the service topology diagram and Rust kernel table]

IMPLICIT: BANZA is a sophisticated payment API with good engineering

DESIRED:
  New opening paragraph before the kernel table:

  "A arquitectura do BANZA é desenhada para impor as garantias do protocolo
   a nível de infraestrutura — não a nível de política. A separação em
   18 crates significa que nenhum operador pode colapsar lógica de ledger
   em lógica de aplicação. O ledger append-only significa que nenhuma
   transacção pode ser silenciosamente modificada. O Rust significa que
   erros de aritmética financeira são impossíveis em tempo de compilação.
   Estas não são escolhas de engenharia — são garantias do protocolo."
```

---

### MSG-ARC-002 (P2) — EMIS/Multicaixa crate context

**Location:** `docs/BANZAMI_REFERENCE.md`, §4 kernel crate table

```
CURRENT:
  | `acquiring` | Integração EMIS/Multicaixa |
  (one table row, no context)

IMPLICIT: BANZA integrates with EMIS (unclear what the relationship is)

DESIRED:
  Add a note below the table:
  "O BANZA opera sobre os carris EMIS para liquidação final — mas adiciona
   a camada de protocolo que o EMIS não fornece: certificação, invariantes
   verificáveis, e regras abertas. O EMIS move dinheiro entre instituições.
   O BANZA define como qualquer operador certificado pode aceder a esses
   movimentos."
```

---

## Cross-Surface: Narrative Hierarchy Insertion Points

The following messages can be inserted verbatim on any surface that lacks the narrative hierarchy. They are short enough to be footers, callouts, or sidebar elements.

### Hierarchy Callout (Short)

```
BANZA é o protocolo. BanzAI é o sistema operativo do protocolo.
Banzami é o operador de referência.
```

### Hierarchy Callout (Medium)

```
BANZA define as regras — um protocolo aberto que qualquer operador certificado implementa.
BanzAI torna o protocolo compreensível — a interface cognitiva que explica, valida e certifica.
Banzami prova que funciona — o primeiro operador, construído pela mesma organização que definiu o protocolo.
```

### One-Sentence Thesis

```
BANZA é a camada de protocolo aberta que Angola precisava — o que o Pix construiu para o Brasil e o UPI para a Índia.
```

### Five-Part Thesis Block

```
Angola tem carris de liquidação.
Angola tem produtos de pagamento.
O que Angola não tinha era uma camada de protocolo aberta.
BANZA é essa camada.
Banzami é a implementação de referência. BanzAI é o sistema operativo do protocolo.
```

---

## Forbidden Implicit Messages (To Audit Against)

The following implicit messages are the result of the narrative substitution patterns identified in the convergence audit. After execution, none should be the conclusion a visitor reaches.

| Forbidden implicit message | Surfaces that currently produce it |
|---------------------------|-------------------------------------|
| "BANZA is a QR payment app" | Homepage (QR + wallet + use case sections), Comerciantes |
| "Banzami is BANZA" | Anywhere Banzami features appear without BANZA framing |
| "BanzAI is a payment chatbot" | /banzamia interface (no landing state) |
| "BANZA is a payment network with certified partners" | /operators (no open protocol argument) |
| "The validation page is a development bug tracker" | /validacao (no transparency claim) |
| "BanzAI is BANZA's future" | /roadmap (no BANZA protocol roadmap) |
| "BANZA is similar to M-Pesa" | §15 (named together without distinction) |
| "BANZA is a payment API" | /banzami-para-programadores (SDK-first without context) |

Every execution change should be evaluated against this list. If the change leaves any item on this list intact on the target surface, the change is incomplete.

---

*Rewrite map completed: 2026-05-30. No modifications applied. Total mapped messages: 24 (8×P0, 10×P1, 6×P2).*
