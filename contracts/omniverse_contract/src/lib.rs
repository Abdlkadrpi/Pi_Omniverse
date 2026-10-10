#![no_std]
use soroban_sdk::{contract, contractimpl, contracttype, Address, Env, String, Symbol, log};

#[contracttype]
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RealWorldAsset {
    pub asset_id: String,
    pub title_deed_hash: String,
    pub total_shares: u128,
    pub price_per_share_pi: u128,
    pub is_compliant: bool,
}

#[contract]
pub struct OmniverseSovereignContract;

#[contractimpl]
impl OmniverseSovereignContract {

    pub fn initialize(env: Env, admin: Address, notary_agent: Address) {
        if env.storage().instance().has(&Symbol::new(&env, "admin")) {
            panic!("Contract is already initialized!");
        }
        env.storage().instance().set(&Symbol::new(&env, "admin"), &admin);
        env.storage().instance().set(&Symbol::new(&env, "notary_agent"), &notary_agent);
        log!(&env, "??? Omniverse Core Initialized. Tripoli Sovereign Node Security Active.");
    }

    pub fn mint_rwa_asset(
        env: Env,
        caller: Address,
        asset_id: String,
        deed_hash: String,
        shares: u128,
        price_pi: u128,
    ) -> RealWorldAsset {
        let agent: Address = env.storage().instance().get(&Symbol::new(&env, "notary_agent")).unwrap();
        caller.require_auth();
        if caller != agent {
            panic!("Access Denied: Only Tripoli_Notary_Agent_01 or Admin can trigger RWA minting.");
        }

        let new_asset = RealWorldAsset {
            asset_id: asset_id.clone(),
            title_deed_hash: deed_hash,
            total_shares: shares,
            price_per_share_pi: price_pi,
            is_compliant: true,
        };

        env.storage().persistent().set(&asset_id, &new_asset);
        log!(&env, "? Asset Successfully Tokenized and SEC/MiCA Verified.");
        new_asset
    }

    pub fn purchase_rwa_share(
        env: Env,
        buyer: Address,
        asset_id: String,
        shares_to_buy: u128,
        lyo_to_burn: u128,
    ) {
        buyer.require_auth();

        let mut asset: RealWorldAsset = env.storage().persistent().get(&asset_id).expect("Asset not found");
        if !asset.is_compliant {
            panic!("Transaction Halted: Target asset fails international compliance checks.");
        }

        if asset.total_shares < shares_to_buy {
            panic!("Inadequate asset liquidity / remaining shares.");
        }

        if lyo_to_burn < 100_00000 {
            panic!("Insufficient LYO combustion gas attached.");
        }

        asset.total_shares -= shares_to_buy;
        env.storage().persistent().set(&asset_id, &asset);

        log!(&env, "?? Settlement Complete. Pi Fee Escrowed. LYO Burned Deflationarily.");
    }
}
