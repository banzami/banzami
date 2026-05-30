# BANZA — Arquitectura do Sistema

> This document describes: **BANZA** — the open financial infrastructure protocol.
> For other layers: [BanzAI](../banzai/BANZAI_REFERENCE.md) · [Banzami](../banzami/BANZAMI_REFERENCE.md)

**Version:** 1.0  
**Date:** 2026-05-30  
**Status:** Official  
**Authority:** ADR-025

---

## Identidade da Rede

O BANZA é uma **rede de pagamentos wallet-native**. Esta é a restrição arquitectónica fundamental da qual todas as decisões de design derivam.

| O BANZA é | O BANZA não é |
|-----------|---------------|
| Rede de transferência instantânea carteira ↔ carteira | Processador de cartões |
| Ecossistema de pagamentos QR-native | Clone do Stripe |
| Sistema de identidade @handle | Gateway Visa/Mastercard |
| Rede monetária Kwanza-native | Plataforma de checkout card-first |
| Integração de carris locais (EMIS, Multicaixa Express) | Cópia de modelo ocidental |

A operação canónica de pagamento:

```
Consumer Wallet ──[ledger transfer]──▶ Merchant Wallet
```

A experiência canónica: `SCAN QR → CONFIRM → INSTANT SETTLEMENT`

Modelos de referência: **Pix, WeChat Pay, M-Pesa, UPI** — não Stripe checkout.

---

## Kernel BANZA

O Kernel BANZA é o núcleo financeiro escrito em **Rust**. É composto por crates com responsabilidades rigorosamente separadas:

| Crate | Responsabilidade |
|-------|-----------------|
| `banzami-ledger` | Motor de contabilidade de dupla entrada — a fonte de verdade financeira |
| `banzami-wallets` | Estado de carteira, reservas, lógica de saldo disponível |
| `banzami-transactions` | Máquina de estados de transacção (PENDING → CAPTURED → SETTLED) |
| `banzami-transfers` | Motor de transferência P2P |
| `banzami-qr` | Domínio de pagamento QR (estático, dinâmico, de uso único) |
| `banzami-settlement` | Orquestração de liquidação e modelo de taxas |
| `banzami-routing` | Encaminhamento de pagamentos baseado em capacidades |
| `banzami-acquiring` | Abstracção de provider de aquisição |
| `banzami-reconciliation` | Reconciliação e verificação de liquidação |
| `banzami-payouts` | Orquestração de payouts para carris bancários |
| `banzami-types` | Tipos partilhados: `Money`, `WalletId`, `TransactionId`, `TraceId` |

### Por que Rust

Segurança de memória sem garbage collector. Comportamento determinístico. Abstrações de custo zero. Zero overhead para garantias de segurança de tipos.

O Kernel nunca contém lógica de negócio de operadores. Os operadores nunca modificam invariantes do Kernel. Esta fronteira é permanente e imposta por revisão de código.

---

## Camadas de Protocolo

O protocolo BANZA opera em quatro camadas:

| Camada | Função |
|--------|--------|
| **Camada Física** | Banks, EMIS, settlement rails, infraestrutura de liquidação |
| **Camada Financeira** | Kernel BANZA em Rust. Ledger, wallets, transactions, settlement, QR, payouts. Executa regras com precisão determinística. |
| **Camada de Governança** | Certificação, conformidade, federação. RFCs, ADRs, validation matrix, manifestos de operador. |
| **Camada Cognitiva** | BanzAI — interface humana do protocolo. Ver [BANZAI_REFERENCE.md](../banzai/BANZAI_REFERENCE.md). |

---

## Contratos Públicos

Os contratos do protocolo definem a superfície pública que qualquer implementação deve respeitar:

| Directório | Conteúdo |
|------------|---------|
| `contracts/openapi/` | Especificação OpenAPI — shape das APIs |
| `contracts/webhooks/` | Esquemas de payload de webhooks |
| `contracts/qr/` | Formato de payload QR (`BANZAMI-SBX:` e `BANZAMI:`) |
| `contracts/sdk-certification/` | Vectores de certificação de SDK |

Mudanças a contratos públicos requerem um ADR e um período de revisão mínimo de 7 dias. Ver [BANZA_GOVERNANCE.md](BANZA_GOVERNANCE.md).

---

## Modelo de Provider

O Kernel BANZA define traits de provider que qualquer operador implementa. Os providers são a fronteira entre o protocolo e a infraestrutura específica do operador.

```
Kernel (protocol rules)
    ↓ defines traits
AcquirerProvider          ← operadores implementam
SettlementExecutionProvider ← operadores implementam
NotificationProvider       ← operadores implementam
```

Esta arquitectura garante que o Kernel nunca contém código específico de um operador. O Banzami implementa estes providers — como qualquer outro operador certificado.

Para os providers disponíveis, ver `docs/architecture/provider-model.md`.

---

## Modelo de Capacidades

Os operadores declaram as suas capacidades num manifesto formal. O protocolo define quais as combinações de capacidades que são permitidas e quais os invariantes que cada capacidade deve satisfazer.

```json
{
  "operator_id": "banzami",
  "certification_level": 2,
  "capabilities": {
    "wallet.consumer": true,
    "wallet.merchant": true,
    "qr.static": true,
    "qr.dynamic": true,
    "p2p.transfer": true,
    "payment_links": true,
    "settlement.t0": true
  }
}
```

Ver [BANZA_CERTIFICATION.md](BANZA_CERTIFICATION.md) para os requisitos de cada nível.

---

## Rastreabilidade

Cada evento financeiro carrega um `trace_id`. Cada cadeia causal é reconstituível. Nenhum dinheiro se move sem uma entrada de ledger. Nenhuma entrada de ledger é alguma vez modificada.

```
transfer created    → trace_id: "trc_abc123"
ledger debit        → trace_id: "trc_abc123", causation_id: "trf_001"
ledger credit       → trace_id: "trc_abc123", causation_id: "trf_001"
settlement entry    → trace_id: "trc_abc123", causation_id: "trf_001"
webhook dispatch    → trace_id: "trc_abc123"
```

O invariante `INV-TRACE-001` impõe que todos os artefactos numa cadeia causal partilhem o mesmo `trace_id`.

---

## Invariantes Financeiros

Os invariantes financeiros são propriedades do protocolo — não de nenhum operador. Estão definidos canonicamente em [BANZA_REFERENCE.md §7](BANZA_REFERENCE.md).

| Invariante | Descrição |
|-----------|-----------|
| `INV-LEDGER-001` | Débito total = Crédito total (soma-zero) |
| `INV-LEDGER-002` | Entradas de ledger são imutáveis após criação |
| `INV-LEDGER-003` | Todos os valores monetários são inteiros (sem vírgula flutuante) |
| `INV-LEDGER-004` | O posting é atómico — nunca parcialmente aplicado |
| `INV-WALLET-001` | `balance = available + reserved` em todos os momentos |
| `INV-STL-001` | `gross_minor = net_minor + fee_minor` (sem criação de dinheiro) |
| `INV-STL-002` | Sem saldos negativos em nenhuma carteira |

O Kernel impõe estes invariantes em Rust. Nenhum operador pode desactivá-los.

---

## Representação Monetária

A aritmética de vírgula flutuante é proibida para dinheiro. Todos os valores monetários são inteiros em unidades menores (centavos / menor unidade da moeda).

```rust
// CORRECTO — inteiros em unidades menores
let amount: i64 = 2500_00; // 2.500,00 Kz (kwanza e cêntimos)

// PROIBIDO — vírgula flutuante
let amount: f64 = 2500.00; // NEVER
```

Convenção de nomenclatura obrigatória: todos os campos de montante usam o sufixo `_minor`.

```json
{ "amount_minor": 250000, "currency": "AOA" }
```

Ver [BANZA_REFERENCE.md §6](BANZA_REFERENCE.md) para a especificação normativa completa.

---

## Ciclo de Vida de Pagamento

```
Customer initiates payment
    ↓
Risk check (synchronous)
    ↓
Compliance check (synchronous)
    ↓
Ledger posting (atomic, synchronous)
    ↓
Wallet balance update (synchronous)
    ↓
Transfer status → COMPLETED
    ↓
Webhook dispatch (begins immediately after commit)
    ↓
Async: retries, reconciliation, analytics, reporting
```

**Regra crítica:** As escritas de ledger permanecem síncronas e atómicas. As filas NUNCA são usadas para a confirmação principal de pagamento. Latência alvo: <2 segundos.

---

## Certificação e Conformidade

O protocolo define cinco níveis de certificação (L0–L4) que os operadores devem alcançar para participar no ecossistema. A certificação é verificada por uma suite de testes determinística, não por declaração própria.

Ver [BANZA_CERTIFICATION.md](BANZA_CERTIFICATION.md) para os requisitos completos.  
Ver [BANZA_CONFORMANCE.md](BANZA_CONFORMANCE.md) para a suite de testes.

---

## Federação

A federação é uma camada de primeira classe na arquitectura BANZA. Define como operadores certificados comunicam, encaminham pagamentos e liquidam entre si. Operadores com Certificação Nível 3+ (Federation Operator) podem participar.

Estado actual: fase de desenho. Ver [BANZA_REFERENCE.md §10](BANZA_REFERENCE.md) para o roadmap de federação.

---

## Implementação de Referência

O Banzami é a implementação de referência do protocolo BANZA. A sua arquitectura técnica está documentada em [BANZAMI_ARCHITECTURE.md](../banzami/BANZAMI_ARCHITECTURE.md).

O Kernel BANZA é desenvolvido no repositório `~/banza`. O Banzami implementa-o em `~/banzami`. Estas são responsabilidades separadas com repositórios separados.

---

**Referências:**

- ADR-001 — Go/Rust service boundary
- ADR-002 — Double-entry ledger
- ADR-006 — QR payment system
- ADR-013 — Wallet-native identity
- ADR-018 — Open financial kernel
- ADR-019 — Operator separation
- ADR-025 — Ecosystem naming inversion

Ver também:
- [BANZA_REFERENCE.md](BANZA_REFERENCE.md) — Canonical protocol reference
- [BANZA_CERTIFICATION.md](BANZA_CERTIFICATION.md) — Certification levels L0–L4
- [BANZA_CONFORMANCE.md](BANZA_CONFORMANCE.md) — Conformance suite
- `docs/architecture/` — Detailed per-domain architecture
