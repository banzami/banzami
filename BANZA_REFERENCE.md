# BANZA — Documento de Referência do Protocolo

**Version:** 1.0  
**Date:** 2026-05-30  
**Status:** Official  
**Authority:** ADR-025

---

## Ecosystem Hierarchy

```
BANZA    = open financial infrastructure protocol        ← THIS DOCUMENT
BanzAI   = Protocol Operating System
the reference operator  = reference operator implementation
```

## Scope

This document defines only: **the BANZA open financial infrastructure protocol** — its rules, invariants, governance, certification, and federation model.

Anything outside this scope is defined in:
- [BANZAI_REFERENCE.md](../banzai/BANZAI_REFERENCE.md) — The BanzAI Protocol OS
- [BANZA_REFERENCE.md](../banza/BANZA_REFERENCE.md) — The the reference operator reference operator

---

## Índice

### Parte I — O Problema e a Solução
1. O Problema: Angola Tem as Peças
2. A Camada que Falta
3. O que é o BANZA

### Parte II — Arquitectura do Protocolo
4. Princípios Fundamentais
5. Arquitectura do Ecossistema
6. Representação Monetária (Normativa)
7. Invariantes Financeiros

### Parte III — Governança e Certificação
8. Governança do Protocolo
9. Modelo de Certificação
10. Federação

### Parte IV — Visão
11. Roadmap do Protocolo
12. Declaração de Visão

---

## 1. O Problema: Angola Tem as Peças

Angola tem bancos. Vinte e três instituições financeiras licenciadas. Um sistema de liquidação interbancária — o EMIS. Redes de caixas automáticos. Aplicações de homebanking. O Multicaixa. Dezasseis milhões de pessoas com telemóvel.

Angola tem as peças. O que Angola não tem é a camada que as conecta.

### O que existe não é suficiente

Para integrar pagamentos, uma empresa tem de estabelecer um acordo bilateral com um banco. O processo pode demorar meses. A documentação é privada. Os termos são negociados caso a caso. O acesso é discricionário — não existe um conjunto de regras públicas que qualquer entidade possa ler e implementar.

Para processar pagamentos de forma independente, uma fintech tem de se tornar banco. Para que carteiras de operadores diferentes comuniquem entre si, não existe mecanismo — cada rede é fechada sobre si mesma.

### Os sintomas visíveis

**Comprovativo por WhatsApp.** Capturas de ecrã de transferências bancárias como prova de pagamento — porque não existe alternativa com garantia de protocolo.

**Integração fechada.** Uma empresa integra-se com o sistema de um banco específico. Essa integração não funciona com outro banco. Não existe uma interface standard que qualquer banco respeite — porque não existe um protocolo que o exija.

**Exclusão da pequena empresa.** Um terminal POS exige contrato de aquisição, hardware e taxas mensais. Uma mercearia de bairro não tem condições.

**Dependência de redes proprietárias.** Cada plataforma funciona segundo as suas próprias regras. Um operador pode alterar taxas, desligar funcionalidades, ou encerrar sem aviso.

**Ausência de garantias de protocolo.** A liquidação instantânea é uma promessa contratual — não um invariante verificável por auditores independentes.

### A causa

Angola tem rails de liquidação — o EMIS resolve o movimento final entre bancos. Não resolve: quem pode aceder ao sistema de pagamentos, em que condições, e segundo que regras verificáveis.

Esta camada tem um nome: **camada de protocolo**.

> Esse é o vazio que o BANZA preenche. Não como banco. Não como produto fintech. Como protocolo.

---

## 2. A Camada que Falta

Uma camada de protocolo não é um produto. Não é uma aplicação. Não é uma empresa. É um conjunto de regras abertas — definidas por uma entidade de governança, publicadas para qualquer entidade ler, implementáveis por qualquer entidade que passe a certificação.

### Dois modelos

**O modelo fechado: M-Pesa**

O M-Pesa pertence à Safaricom. As regras são do operador. Quando a Safaricom decide alterar preços, todos os utilizadores ficam sujeitos. Quando decide encerrar o serviço num país, o serviço encerra. Uma startup que quer construir sobre o M-Pesa precisa de um acordo nas condições que o operador decidir.

O M-Pesa é um produto extraordinário. Mas é um produto — não um protocolo. A rede pertence ao operador.

**O modelo aberto: Pix e UPI**

O Banco Central do Brasil não criou um produto — criou um protocolo. O Nubank implementa o Pix. O Itaú implementa o Pix. O Google Pay implementa o Pix. Centenas de entidades implementam o Pix — cada uma com o seu produto, a sua experiência, o seu modelo de negócio — mas todas segundo as mesmas regras abertas. Nenhuma delas é dona do Pix.

Em menos de dois anos, o Pix tornou-se o método de pagamento mais utilizado no Brasil.

A India Payments Corporation seguiu o mesmo modelo com o UPI em 2016. Em 2024, o UPI processava mais de 15 mil milhões de transacções mensais.

### A diferença estrutural

| | M-Pesa | Pix / UPI | BANZA |
|---|---|---|---|
| **Quem define as regras** | O operador | Entidade de governança | Protocolo aberto (RFCs e ADRs) |
| **Quem pode participar** | Entidades com acordo com o operador | Qualquer entidade certificada | Qualquer entidade certificada |
| **Pode um terceiro tornar-se operador independente?** | Não | Sim | Sim |

### O que acontece se um operador desaparecer?

Este é o teste definitivo.

No modelo fechado: se o operador principal desaparece, o sistema desaparece.

No modelo aberto: se um operador desaparece, os outros continuam. O Pix não pertence ao Nubank. Se o Nubank desaparecesse amanhã, o Pix continuaria.

**O BANZA segue o modelo aberto.**

As regras do protocolo BANZA são públicas. O operador é o primeiro operador certificado e a implementação de referência — mas não é o dono do protocolo. Se o operador desaparecesse amanhã: as regras do protocolo BANZA continuariam a existir. Os outros operadores certificados continuariam a operar. A infraestrutura permaneceria.

Isto não é uma propriedade acidental. É uma decisão de arquitectura deliberada.

---

## 3. O que é o BANZA

O BANZA é o protocolo aberto de pagamentos digitais que Angola não tinha — a camada de infraestrutura certificada que qualquer programador, operador ou instituição pode implementar, da mesma forma que o Pix construiu o ecossistema de pagamentos do Brasil e o UPI construiu o da Índia.

### Arquitectura de três níveis

```
BANZA
│  O protocolo. Regras abertas. Certificação acessível. Invariantes verificáveis.
│  Define como o dinheiro se move digitalmente em Angola.
│  Qualquer entidade certificada pode implementar e operar sobre ele.
│
├── BanzAI
│   O Sistema Operativo do protocolo.
│   Torna o BANZA acessível a operadores, programadores, reguladores e auditores.
│   Não é um chatbot. É infraestrutura cognitiva do protocolo.
│   Ver: BANZAI_REFERENCE.md
│
└── the reference operator
    A implementação de referência.
    O primeiro operador certificado BANZA.
    Um operador entre futuros muitos — não o dono do protocolo.
    Ver: BANZA_REFERENCE.md
```

Esta arquitectura está definida no ADR-025 (2026-05-29), que supersede o ADR-016.

### O que é o BANZA — quatro propriedades concretas

**Regras públicas.** A especificação do BANZA — os RFCs, os ADRs, o conformance suite — está disponível para qualquer programador ler, qualquer operador implementar, e qualquer auditor inspeccionar. Nenhuma documentação está fechada atrás de um acordo de confidencialidade.

**Certificação aberta.** Qualquer entidade legal que passe o conformance suite torna-se um operador certificado BANZA. Não existe processo de acreditação institucional. Não existe acordo bilateral. O acesso à certificação é definido pelas regras do protocolo.

**Invariantes verificáveis.** As propriedades financeiras do protocolo são impostas pelo kernel e verificáveis por qualquer auditor independentemente de qualquer operador. A liquidação em T+0 é um invariante do kernel Rust: o código não pode completar uma transacção que viole esta propriedade.

**Federação.** Operadores certificados podem encaminhar pagamentos entre si sem acordos bilaterais — porque ambos implementam o mesmo protocolo aberto.

### O que o BANZA não é

| O BANZA não é | Porquê a distinção importa |
|---|---|
| **Um banco** | O BANZA define regras que operadores seguem. Não detém dinheiro de ninguém. |
| **Um produto fintech** | Um produto pertence ao seu operador. O protocolo pertence à infraestrutura. |
| **Uma API fechada** | A especificação do BANZA é pública. Nenhum operador pode alterá-la unilateralmente. |
| **O operador** | O operador é um operador — o primeiro e a implementação de referência. Não é o protocolo. |

### Os quatro princípios do protocolo

Qualquer operador certificado BANZA implementa estes quatro princípios. Não são funcionalidades do operador. São invariantes do protocolo — propriedades que qualquer implementação deve garantir para ser certificada.

| Princípio | O que o protocolo garante |
|---|---|
| **Wallet-native** | Cada conta é uma carteira. Pagamentos são transferências directas — sem IBAN, sem intermediário de liquidação adicional. |
| **QR-native** | O QR é a superfície primária de pagamento definida pelo protocolo. Um operador certificado que não exponha a superfície QR não está em conformidade. |
| **Programmable** | A integração programática via SDK é um requisito do protocolo — não uma funcionalidade opcional. |
| **Instant settlement** | A liquidação em T+0 é um invariante do protocolo — verificável no kernel, não dependente da política de nenhum operador. |

### A distinção fundamental: protocolo ≠ operador

O protocolo define as regras. O operador implementa-as.

O protocolo existe independentemente de qualquer operador. Se todos os operadores actuais desaparecessem amanhã, o protocolo — as regras, a especificação, o conformance suite — continuaria a existir.

A relação é exactamente a que existe entre o Pix e o Nubank. O Nubank é o maior utilizador do Pix no Brasil — mas o Pix não pertence ao Nubank.

### O nome

**Banza** e **the reference operator** são palavras enraizadas nas tradições linguísticas bantu de Angola, especialmente no universo Kikongo, onde *mbanza* designa um lugar de encontro — um centro de vida comunitária. Nomes distintamente angolanos — não palavras emprestadas de outro continente.

---

## 4. Princípios Fundamentais

### A correcção financeira não é negociável

Cada decisão de engenharia é avaliada contra: "Isto preserva a correcção financeira?" A simplicidade operacional e a auditabilidade superam funcionalidades.

### O protocolo é o produto

O operador (o produto de consumo) é a implementação de referência do protocolo BANZA. O protocolo é o que escala. O operador é o que prova que funciona.

### Os operadores implementam política. O Kernel implementa o protocolo.

O Kernel BANZA impõe os invariantes financeiros. Os operadores aplicam as suas políticas de negócio dentro das restrições que o kernel impõe. Estas camadas nunca se colapsam.

### Rastreabilidade por defeito

Cada evento financeiro carrega um `trace_id`. Cada cadeia causal é reconstituível. Nenhum dinheiro se move sem uma entrada de ledger. Nenhuma entrada de ledger é alguma vez modificada.

### Angola primeiro

O protocolo foi desenhado em torno do Kwanza, da lei comercial angolana, dos carris EMIS e do sector informal que representa a maioria do comércio angolano.

---

## 5. Arquitectura do Ecossistema

### Kernel BANZA

O Kernel BANZA é o núcleo financeiro escrito em Rust. É composto por crates com responsabilidades rigorosamente separadas:

| Crate | Responsabilidade |
|---|---|
| `ledger` | Motor de ledger de dupla entrada — append-only, balanceado, atómico |
| `wallets` | Ciclo de vida de carteiras de comerciantes |
| `consumer-wallets` | Ciclo de vida de carteiras de consumidores |
| `transactions` | Estado de máquina de transacções |
| `transfers` | Transferências wallet-to-wallet |
| `settlement` | Liquidação T+0 e ciclos de payout |
| `reconciliation` | Reconciliação automatizada |
| `payouts` | Saídas para contas bancárias |
| `qr` | Sistema QR estático e dinâmico |
| `identity` | Handle @banza, registo e unicidade |
| `risk` | Motor de avaliação de risco |
| `compliance` | Regras de conformidade regulatória |
| `routing` | Encaminhamento de pagamentos |

### Operadores

Um Operador é qualquer entidade que implementa o protocolo BANZA para processar pagamentos. Os operadores:
- Declaram capacidades num Manifesto de Operador
- Implementam os requisitos de conformidade para o seu nível de certificação
- Operam dentro do framework de invariantes
- Estão sujeitos a verificação de certificação periódica

**Operador de Referência:** The reference operator do protocolo completo. Ver [BANZA_REFERENCE.md](../banza/BANZA_REFERENCE.md).

**Operadores Certificados:** Qualquer entidade que obtenha certificação BANZA pode implementar o protocolo. Operadores certificados são o resultado intencional do protocolo — não um conceito futuro.

### Stack Tecnológico do Protocolo

| Camada | Tecnologia | Justificação |
|---|---|---|
| Núcleo financeiro | Rust | Segurança de memória, performance determinística |
| Orquestração | Go | Simplicidade operacional, concorrência |
| Persistência (referência) | PostgreSQL | Garantias ACID — implementação de referência; o protocolo é agnóstico ao storage |
| Cache / coordenação | Redis | Rate limiting, idempotência, sessões |
| Observabilidade | OpenTelemetry | Traces, métricas e logs vendor-neutral |

---

## 6. Representação Monetária (Normativa)

> **Esta secção é normativa.** Todos os operadores, SDKs e implementações do protocolo BANZA DEVEM conformar com estas regras.

### Regra de Inteiros

**Todos os valores monetários no protocolo BANZA DEVEM ser representados como inteiros.**

Valores monetários em vírgula flutuante são proibidos em toda a superfície do protocolo, incluindo: APIs, traces e logs, manifestos de operador, saldos de carteiras, entradas de ledger, batches de liquidação, contratos de SDK.

**Exemplos proibidos:**
```json
{ "amount": 10.50 }
```

**Exemplos válidos:**
```json
{ "amount_minor": 1050 }
```

### Convenção `*_minor`

O protocolo BANZA adopta a convenção `*_minor` para todos os campos monetários:

| Campo | Significado |
|---|---|
| `amount_minor` | Valor genérico de pagamento |
| `gross_minor` | Montante bruto pago pelo consumidor |
| `fee_minor` | Taxa retida pelo operador |
| `net_minor` | Montante líquido entregue ao receptor |
| `available_minor` | Saldo disponível imediatamente |
| `reserved_minor` | Saldo temporariamente bloqueado |
| `balance_minor` | Saldo total da carteira |

### Semântica de Montantes de Liquidação

Todo o fluxo de pagamento BANZA produz três montantes com semântica exacta:

**Invariante normativo (INV-STL-001):**

```
gross_minor = net_minor + fee_minor
```

### Semântica de Saldo de Carteira

**Invariante normativo (INV-WALLET-001):**

```
balance_minor = available_minor + reserved_minor
```

Os saldos de carteiras são sempre derivados de entradas de ledger — nunca directamente mutados. Um saldo de carteira nunca pode ser negativo (INV-STL-002).

### Registo de Moedas

| Moeda | Código ISO 4217 | Minor units | Status |
|---|---|---|---|
| Kwanza Angolano | `AOA` | 100 (1 AOA = 100 minor units) | Moeda oficial BANZA |
| Dólar Americano | `USD` | 100 | Suportado (traces de demonstração) |
| Euro | `EUR` | 100 | Suportado (traces de demonstração) |

Qualquer alteração à política de precisão requer um RFC aprovado.

### Regra de Certificação MON-001

**MON-001 — Representação Monetária em Inteiros**

| Violação | Resultado |
|---|---|
| Valores float em APIs | FAIL de certificação |
| Valores float em traces | FAIL de certificação |
| `gross_minor ≠ net_minor + fee_minor` | FAIL de certificação |
| `balance_minor ≠ available_minor + reserved_minor` | FAIL de certificação |

---

## 7. Invariantes Financeiros

Os invariantes financeiros são afirmações não negociáveis que nunca podem ser violadas. São impostos em múltiplas camadas simultaneamente.

### Famílias de Invariantes

| Família | Exemplos |
|---|---|
| `INV-LEDGER-*` | Dupla entrada, imutabilidade, sem vírgula flutuante, atomicidade |
| `INV-WALLET-*` | Saldo consistente, sem negativos |
| `INV-STL-*` | gross = net + fee, sem criação de dinheiro |
| `INV-TRACE-*` | Completude da rastreabilidade |
| `INV-QR-*` | Ciclo de vida do QR, unicidade de resolução |
| `INV-IDENT-*` | Unicidade de handle |

### Invariantes Críticos

| Invariante | Descrição | Gravidade |
|---|---|---|
| INV-LEDGER-001 | Débitos = Créditos em cada posting | CRITICAL |
| INV-LEDGER-002 | Entradas de ledger são imutáveis | CRITICAL |
| INV-LEDGER-003 | Montantes são i64, nunca float | CRITICAL |
| INV-LEDGER-004 | Postings parciais nunca persistem | CRITICAL |
| INV-STL-001 | gross = net + fee (sem criação de dinheiro) | CRITICAL |
| INV-STL-002 | Saldos nunca negativos | CRITICAL |
| INV-WALLET-001 | balance = available + reserved | CRITICAL |
| INV-IDENT-001 | @banza handles são únicos globalmente | CRITICAL |

### O Ledger de Dupla Entrada

O ledger é:
- **Append-only** — as entradas nunca são modificadas ou eliminadas
- **Balanceado** — cada posting tem débitos e créditos iguais
- **Integer-only** — os montantes são armazenados como i64 minor units, nunca vírgula flutuante
- **Atómico** — postings parciais nunca persistem

O fluxo canónico de um pagamento QR:

```text
Carteira consumidor (DÉBITO)
    ├── Carteira comerciante (CRÉDITO) — montante líquido
    └── Carteira de taxas (CRÉDITO)   — taxa

gross_minor = net_minor + fee_minor  [INV-STL-001]
```

### Rastreabilidade

Cada fluxo de pagamento produz um `trace_id`. O trace captura todos os eventos: `qr.created` → `payment.initiated` → `ledger.posted` → `wallet.updated` → `webhook.dispatched`.

Os traces são a ferramenta de auditoria primária. O BanzAI inclui um módulo Trace Explainer que reconstrói e verifica qualquer trace interactivamente. Ver [BANZAI_REFERENCE.md](../banzai/BANZAI_REFERENCE.md).

---

## 8. Governança do Protocolo

### RFCs (Request for Comments)

Os RFCs governam decisões ao nível do protocolo: invariantes financeiros, fluxos de pagamento, contratos de API, requisitos de operadores, protocolos de federação.

Um RFC é obrigatório para:
- Qualquer alteração ao conjunto de invariantes financeiros
- Qualquer alteração ao protocolo de fluxo de pagamento
- Qualquer novo nível de certificação
- Qualquer nova moeda no registo oficial
- Design do protocolo de federação

Os RFCs são numerados sequencialmente e imutáveis após aceitação.

### ADRs (Architecture Decision Records)

Os ADRs governam decisões de implementação: escolhas tecnológicas, fronteiras de serviços, arquitectura de SDK, arquitectura de marca, modelo de identidade.

ADR-025 é o ADR canónico que define a hierarquia de três níveis (BANZA / BanzAI / the reference operator). ADR-016 foi supersedido por ADR-025.

### Validation Matrix

O `docs/validation/BANZA_IMPLEMENTATION_MATRIX.json` é a fonte de verdade para o progresso de implementação do operador de referência. Alterações à matrix requerem frases de governança com verificação de fingerprint.

### Domínios de Validação

| Domínio | Âmbito |
|---|---|
| `DOM-FIN` | Integridade financeira (ledger, wallets, liquidação) |
| `DOM-IDENTITY` | Carteira e identidade de consumidor |
| `DOM-CONSUMER` | Experiência do consumidor |
| `DOM-MERCHANT` | Experiência do comerciante |
| `DOM-DEVELOPER` | Experiência do programador (SDK, API) |
| `DOM-INFRA` | Infraestrutura operacional |
| `DOM-SECURITY` | Segurança e autenticação |
| `DOM-COMPLIANCE` | Conformidade regulatória |

---

## 9. Modelo de Certificação

### Níveis de Certificação

| Nível | Nome | Capacidades necessárias |
|---|---|---|
| **L0** | Sandbox Operator | Operações básicas sandbox |
| **L1** | Payment Operator | wallet.consumer, wallet.merchant, qr.static, p2p.transfer |
| **L2** | Settlement Operator | L1 + qr.dynamic, payment_links, settlement.t0 |
| **L3** | Federation Operator | L2 + payout.batch, reconciliation |
| **L4** | Infrastructure Operator | L3 + acquiring.emis, federation_ready |

**Princípio de acesso aberto:** Qualquer entidade legal que passe o conformance suite torna-se um operador certificado. Sem acesso institucional. Sem acordo bilateral. Sem volume mínimo de transacções.

### Manifesto de Operador

```json
{
  "operator_id": "op_example_001",
  "version": "1.0.0",
  "certification_level": 2,
  "capabilities": [
    "wallet.consumer",
    "wallet.merchant",
    "qr.static",
    "qr.dynamic",
    "p2p.transfer",
    "payment_links",
    "settlement.t0"
  ],
  "invariants_asserted": [
    "INV-LEDGER-001",
    "INV-LEDGER-002",
    "INV-STL-001",
    "INV-STL-002"
  ],
  "environment": "LIVE",
  "sandbox_available": true
}
```

### Manutenção de Certificação

- Actualizações major do protocolo requerem re-certificação
- Verificação automática de invariantes mensal
- Spot-checks de conformidade trimestrais
- As certificações expiram após 12 meses sem re-verificação

### O BanzAI e a Certificação

O BanzAI guia operadores no processo de certificação. Não concede a certificação — o conformance suite é o árbitro, porque ferramentas determinam a verdade. Ver [BANZAI_REFERENCE.md](../banzai/BANZAI_REFERENCE.md).

---

## 10. Federação

A federação é uma camada de primeira classe na arquitectura BANZA. Define como operadores certificados comunicam, encaminham pagamentos e liquidam entre si.

### Estado Actual

A federação encontra-se na fase de desenho. Todos os pagamentos são actualmente processados pelo operador de referência the reference operator. O kernel foi desenhado com os primitivos necessários:
- Propagação de `trace_id` através de fronteiras de serviço
- Declaração de manifesto de operador com capacidades de encaminhamento
- Arquitectura de encaminhamento baseada em capacidades
- Isolamento de liquidação entre operadores

### Requisitos para Federação

- Ambos os operadores com Certificação Nível 3+ (Federation Operator)
- Conta de liquidação partilhada com BANZA
- Manifesto de federação com capacidades de encaminhamento
- Propagação cross-operador de trace_id
- Liquidação atómica cross-operador no ledger

### Roadmap de Federação

| Marco | Descrição | Alvo |
|---|---|---|
| RFC de federação | Definir protocolo inter-operadores | H1 2027 |
| Operadores piloto | Dois operadores em federação controlada | H2 2027 |
| Federação aberta | Qualquer operador Nível 4 pode federar | 2028 |

---

## 11. Roadmap do Protocolo

### Curto prazo (H2 2026)

| Item | Descrição |
|---|---|
| Conformance Suite v1 | Suite de testes executável para Níveis 1–3, disponível publicamente |
| Certificação Nível 1–2 | Primeiros operadores externos certificados |
| Documentação de certificação open access | Processo de certificação documentado publicamente |

### Médio prazo (H1 2027)

| Item | Descrição |
|---|---|
| Certificação Nível 3–4 | Protocolo completo e certificação de infraestrutura |
| Operadores de terceiros | Primeiros operadores externos no protocolo |
| RFC de federação | Especificação de encaminhamento inter-operadores |
| Portal de certificação | Certificação self-service para operadores |

### Longo prazo (H2 2027+)

| Item | Descrição |
|---|---|
| Piloto de federação | Dois operadores em federação controlada |
| Federação aberta | Qualquer operador Nível 4 pode federar |
| Carris cross-border | AOA ↔ outras moedas africanas |
| RFC process aberto à comunidade | Contribuições externas ao protocolo |

---

## 12. Declaração de Visão

O ecossistema de pagamentos digitais de Angola será construído sobre o protocolo BANZA — não sobre o produto de um único operador.

O ecossistema tem sucesso quando:
- Qualquer programador pode construir sobre o protocolo
- Qualquer operador pode certificar-se
- Qualquer angolano pode transaccionar, independentemente de qual operador usa

**O protocolo é o que fica.**

Os operadores mudam. Os produtos evoluem. O que o BANZA garante é que as regras permaneçam abertas, a certificação permaneça acessível, e a infraestrutura permaneça de Angola.

> **BANZA é o protocolo. BANZA move o dinheiro. O protocolo existe independentemente de qualquer operador.**

---

**Referências:**

- ADR-025 — Hierarquia canónica de três níveis (supersede ADR-016)
- ADR-002 — Ledger de dupla entrada
- ADR-004 — Idempotência e rate limiting
- ADR-006 — Sistema de pagamento QR
- ADR-012 — Ecossistema SDK-first
- ADR-013 — Identidade wallet-native
- ADR-018 — Open financial kernel
- ADR-019 — Operator separation
- ADR-024 — Reference operator

Ver também:
- [BANZAI_REFERENCE.md](../banzai/BANZAI_REFERENCE.md) — Protocol Operating System
- [BANZA_REFERENCE.md](../banza/BANZA_REFERENCE.md) — Reference operator implementation
