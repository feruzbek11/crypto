import secrets
import eth_keys
from web3 import AsyncWeb3
import asyncio

count_dict = {'count': 0}
current_node_index = 0

def generate_key_pair():
    private_key = secrets.token_hex(32)
    private_key_bytes = bytes.fromhex(private_key)
    public_key_hex = eth_keys.keys.PrivateKey(private_key_bytes).public_key
    public_key_bytes = bytes.fromhex(str(public_key_hex)[2:])
    public_address = eth_keys.keys.PublicKey(public_key_bytes).to_address()
    return public_address, private_key

async def get_transaction_count(w3, address):
    transaction_count = await w3.eth.get_transaction_count(address)
    return transaction_count

async def check_addr(w3, nodes, file_path):
    global current_node_index
    while True:
        try:
            address, private_key = generate_key_pair()
            address = w3.to_checksum_address(address)
            transaction_count = await get_transaction_count(w3, address)

            count_dict['count'] += 1
            print(f'{count_dict["count"]}.{transaction_count} TX | {address} | {private_key}')
            
            if transaction_count != 1: #поставь 1 для проверики записи в файл
                with open(file_path, 'a') as file:
                    file.write(f'{transaction_count} TX | {address}\t{private_key}\n')
        except Exception as e:
            await switch_node(w3, nodes)
            current_node_index = (current_node_index + 1) % len(nodes)

async def switch_node(w3, nodes):
    global current_node_index
    for _ in range(len(nodes)):
        try:
            node = nodes[current_node_index]
            w3.provider = AsyncWeb3.AsyncHTTPProvider(node)
            await w3.eth.get_block('latest')
            return
        except Exception as e:
            current_node_index = (current_node_index + 1) % len(nodes)
    await asyncio.sleep(60)

async def main():
    # Список серверов
    nodes = [
'https://eth-mainnet.gateway.pokt.network/v1/5f3453978e354ab992c4da79',
'https://eth-mainnet.public.blastapi.io',
'https://1rpc.io/eth',
'https://api.securerpc.com/v1',
'https://ethereum.publicnode.com',
'https://yolo-intensive-paper.discover.quiknode.pro/45cad3065a05ccb632980a7ee67dd4cbb470ffbd',
'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161',
'https://eth-mainnet.alchemyapi.io/v2/QKMdAyFAARxN-dEm_USOu8-u0klcBuTO',
'https://eth.public-rpc.com',
'https://mainnet-eth.compound.finance',
'https://eth.llamarpc.com',
'https://endpoints.omniatech.io/v1/eth/mainnet/public',
'https://rpc.builder0x69.io',
'https://rpc.mevblocker.io',
'https://virginia.rpc.blxrbdn.com',
'https://uk.rpc.blxrbdn.com',
'https://singapore.rpc.blxrbdn.com',
'https://eth.rpc.blxrbdn.com',
'https://eth-pokt.nodies.app',
'https://rpc.payload.de',
'https://eth.api.onfinality.io/public',
'https://core.gashawk.io/rpc',
'https://rpc.eth.gateway.fm',
'https://eth.drpc.org',
'https://mainnet.gateway.tenderly.co',
'https://gateway.tenderly.co/public/mainnet',
'https://eth-mainnet.diamondswap.org/rpc',
'https://rpc.notadegen.com/eth',
'https://rpc.lokibuilder.xyz/wallet',
'https://rpc.flashbots.net/fast',
'https://rpc.mevblocker.io/fast',
'https://rpc.mevblocker.io/noreverts',
'https://rpc.mevblocker.io/fullprivacy']
    #получаем путь к файлу для записи
    file_path = input("Укажите путь к файлу TX.txt: ")
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(nodes[0]))
    await asyncio.gather(*[check_addr(w3, nodes, file_path) for _ in range(50)]) #количество запросов на сервер

asyncio.run(main())
