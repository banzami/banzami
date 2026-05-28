//! Operator and wallet capability declarations for the Banzami kernel.
//!
//! This crate defines declarative capability types that operators and wallets
//! use to announce what they support. The kernel consults these declarations
//! before initiating any flow, enabling graceful degradation and optional
//! feature negotiation.
//!
//! # Design principles
//!
//! - **Declarative**: Capabilities are data, not dynamic method dispatch.
//! - **Discoverable**: All capability structs are serializable to JSON.
//! - **Extensible**: New capability fields use `Option<T>` and carry a `version`
//!   number so older implementations do not break when new capabilities are added.
//! - **Operator-neutral**: No field assumes a specific operator, geography, or
//!   regulatory regime.
//! - **Version-aware**: Every capability set carries a `version: u32` that
//!   increments when new fields are added.
//!
//! # Relationship to RFCs
//!
//! - [`WalletCapabilitySet`] implements RFC-0003 (Wallet Capabilities).
//! - [`ProviderCapabilityDescriptor`] implements RFC-0004 (Provider Capability
//!   Negotiation).
//! - [`OperatorManifest`] lays the groundwork for RFC-0005 (Operator Discovery).

pub mod operator;
pub mod provider;
pub mod wallet;

pub use operator::{OperatorCapabilities, OperatorManifest};
pub use provider::{ProviderCapabilityDescriptor, ProviderKind};
pub use wallet::{WalletCapabilitySet, WalletKind};
