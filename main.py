from seahorse.prelude import *

declare_id('Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS')

class FoodProfile(Account):
    owner: Pubkey  # 32 bytes
    origin: Pubkey  # Public key of the creator
    food_type_u16_32_array: Array[u16, 32]  # 64 bytes
    creation_time: i32  # Creation time as timestamp (i32)
    expiration_date: i32  # Expiration date as timestamp (i32)
    harvest_time: i32  # Harvest time as timestamp (i32)
    transport_log_coordinate_lat: f64  # Single transport log entry
    transport_log_coordinate_long: f64
    transport_log_time: i32

@instruction
def create_food_profile(
    payer: Signer,
    owner: Signer,
    food_profile: Empty[FoodProfile],
    food_type_u16_32_array: Array[u16, 32],
    creation_time: i32,
    expiration_date: i32,
    harvest_time: i32,
    transport_log_coordinate_lat: f64,  # Single transport log entry
    transport_log_coordinate_long: f64,
    transport_log_time: i32,
    seed_random: u128
):
    food_profile = food_profile.init(
        payer=payer,
        seeds=[owner.key(), "food_profile", seed_random],
        space=32 + 64 + 4 + 32 + 4 + 4 + (8 + 8 + 4)  # Adjusted space for single TransportLog entry
    )

    food_profile.owner = owner.key()
    food_profile.origin = payer.key()  # Set the origin to the creator's public key
    food_profile.food_type_u16_32_array = food_type_u16_32_array
    food_profile.creation_time = creation_time
    food_profile.expiration_date = expiration_date
    food_profile.harvest_time = harvest_time

    # Initialize the transport log with the default TransportLog entry
    food_profile.transport_log_coordinate_lat = transport_log_coordinate_lat
    food_profile.transport_log_coordinate_long = transport_log_coordinate_long
    food_profile.transport_log_time = transport_log_time

    print(f'Food Profile created at {food_profile.key()}')

@instruction
def get_food_profile(food_profile: FoodProfile):
    print(f'Owner: {food_profile.owner}')
    print(f'Food Type Array: {food_profile.food_type_u16_32_array}')
    print(f'Origin: {food_profile.origin}')
    print(f'Creation Time: {food_profile.creation_time}')
    print(f'Expiration Date: {food_profile.expiration_date}')
    print(f'Harvest Time: {food_profile.harvest_time}')
    print(f'Transport Log Latitude: {food_profile.transport_log_coordinate_lat}')
    print(f'Transport Log Longitude: {food_profile.transport_log_coordinate_long}')
    print(f'Transport Log Time: {food_profile.transport_log_time}')

@instruction
def transfer_food(
    from_wallet: Signer,
    to_wallet: Pubkey,
    food_profile: FoodProfile,
    food_id_u8_64_array: Array[u8, 64]  # Using Array[char, 32] for food_profile_id
):
    assert from_wallet.key() == food_profile.owner, "Only the owner can transfer this food profile."

    food_profile.owner = to_wallet
    print(f'Food Profile {food_id_u8_64_array} transferred from {from_wallet.key()} to {to_wallet}')

@instruction
def update_transport_log(
    transport_log_coordinate_lat: f64,
    transport_log_coordinate_long: f64,
    transport_log_time: i32,
    food_profile: FoodProfile
):
    # Update the transport log entry directly
    food_profile.transport_log_coordinate_lat = transport_log_coordinate_lat
    food_profile.transport_log_coordinate_long = transport_log_coordinate_long
    food_profile.transport_log_time = transport_log_time
    print(f'Updated transport log to latitude: {transport_log_coordinate_lat}, longitude: {transport_log_coordinate_long}, time: {transport_log_time}')
