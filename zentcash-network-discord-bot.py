import requests
import discord
from functions import json_rpc, getinfo, format_hashrate
from config import BOT_TOKEN
from discord.ext import commands


@commands.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="Zent Cash Network - Help",
        description="**Here is the list of available commands:**",
        color=0x5A9EC9
    )

    embed.add_field(name="!info", value="Displays basic information about Zent Cash.", inline=False)
    embed.add_field(name="!network", value="Displays statistics for the Zent Cash Network.", inline=False)
    embed.add_field(name="!price", value="Get the price of Zent Cash.", inline=False)
    embed.add_field(name="!donate", value="Shows addresses to donate to the project.\n", inline=False)

    embed.set_footer(text="Use the command with '!' followed by the command name.")
    embed.set_thumbnail(url="https://raw.githubusercontent.com/ZentCashFoundation/brand/refs/heads/master/logo/stacked/zentcash_stacked_color.png")
    await ctx.send(embed=embed)



@commands.command(name="info")
async def info_command(ctx):
    embed = discord.Embed(
        title="Zent Cash Network Information",
        description=(
            f"Zent is a useful cryptocurrency for fast, secure and anonymous payments that can be used as a global payment method. Now, the focus of the project aims to create a community related to the gaming sector that uses this currency in a shared and interconnected way with all its platforms. Use all kinds of video games, buy and sell them both in digital and physical format, register in tournaments and win prizes, and give all kinds of solutions to the world of e-sports, all with the same currency, decentralized and with instant transactions.\n\n"
            f" * **[Website](https://zent.cash)**\n"
            f" * **[Wallets CLI](https://github.com/ZentCashFoundation/Zent/releases)**\n"
            f" * **Wallets GUI**\n"
	        f"  - **[Zent Cash Wallet (Suggested)](https://github.com/ZentCashFoundation/zentcash-wallet/releases/tag/v3.4.9)**\n"
	        f"  - **[Zent Cash Wallet Electronic](https://github.com/ZentCashFoundation/zentcash-wallet-electronic/releases/tag/v0.3.15)**\n"
	        f"  - **[Zent Cash Mobile for Android](https://play.google.com/store/apps/details?id=cash.zent.mobileapp)**\n"
	        f" * **[Paper Wallet](https://zentcashfoundation.github.io/zentcash-paper-wallet)**\n"
            f" * **[Pools](https://miningpoolstats.stream/zentcash)**\n"
            f" * **[Explorer](https://explorer.zent.cash/)**\n"
            f" * **[GitHub](https://github.com/ZentCashFoundation)**\n"
            f" * **Social:** \n"
            f"  - **[Discord](https://discord.gg/tfaUE2G)**\n"
            f"  - **[Facebook](https://www.facebook.com/Zent-Cash-Foundation-108069958362688)**\n"
            f"  - **[Youtube](https://www.youtube.com/channel/UCRF0KXM-0UbovyGLpusYjVA?sub_confirmation=1)**\n"
            f"  - **[Twitter](https://twitter.com/ZentCash)**\n"
            f"  - **[Telegram](https://t.me/ZentCashGlobal)**\n"
        ),
        color=0x5A9EC9
    )
    embed.set_thumbnail(url="https://raw.githubusercontent.com/ZentCashFoundation/brand/refs/heads/master/logo/stacked/zentcash_stacked_color.png")
    await ctx.send(embed=embed)

@commands.command(name="network")
async def network_command(ctx):
    networkGetinfo = getinfo()
    last_block_info = json_rpc("getlastblockheader")

    if not last_block_info or "result" not in last_block_info:
        await ctx.send("⚠️ Error fetching the last block header.")
        return

    last_block_hash = last_block_info["result"]["block_header"]["hash"]
    getblock_info = json_rpc("f_block_json", {"hash": last_block_hash})

    # Validar la respuesta de getblock
    if not getblock_info or "result" not in getblock_info:
        await ctx.send("⚠️ Error fetching block details.")
        return

    ticket = "ZTC"
    height = networkGetinfo.get("height", "N/A")
    hashrate = networkGetinfo.get("hashrate", "N/A")
    difficulty = networkGetinfo.get("difficulty", "N/A")
    tx_pool_size = networkGetinfo.get("tx_pool_size", "N/A")
    tx_count = networkGetinfo.get("tx_count", "N/A")
    white_peerlist_size = networkGetinfo.get("white_peerlist_size", "N/A")
    synced = networkGetinfo.get("synced", "N/A")
    version = networkGetinfo.get("version", "N/A")
    total_coins = "7500000000"
    minimum_fee = "10"
    block_header = last_block_info["result"]["block_header"]
    reward = block_header.get("reward", "N/A")
    getblock = getblock_info["result"]["block"]
    alreadyGeneratedCoins = getblock.get("alreadyGeneratedCoins", "N/A")

    try:
        reward = round(float(reward) / 10**2, 2)
        total_coins = round(float(total_coins), 2)
        minimum_fee = round(float(minimum_fee) / 10**2, 2)
        alreadyGeneratedCoins = round(float(alreadyGeneratedCoins) / 10**2, 2)
        hashrate = format_hashrate(hashrate)
    except (ValueError, TypeError):
        reward = "N/A"
        total_coins = "N/A"
        minimum_fee = "N/A"
        alreadyGeneratedCoins = "N/A"

    embed = discord.Embed(
        title="Zent Cash Network Stats",
        description=(
            f"*Block Height:* `{height}`\n"
            f"*Difficulty:* `{difficulty}`\n"
            f"*Hashrate:* `{hashrate}`\n"
            f"*Reward:* `{reward} {ticket}`\n"
            f"*Minimum Network Fee:* `{minimum_fee} {ticket}`\n"
            f"*Mempool TX Count:* `{tx_pool_size}`\n"
            f"*Total TX Count:* `{tx_count}`\n"
            f"*Peers:* `{white_peerlist_size}`\n"
            f"*Synced:* `{synced}`\n"
            f"*Node Version:* `{version}`\n"
            f"*Circulation Emission:* `{alreadyGeneratedCoins} {ticket}`\n"
            f"*Total Coin Supply:* `{total_coins} {ticket}`\n"
            f"*Last Block Hash:* [{last_block_hash}](https://explorer.zent.cash/?hash={last_block_hash}#blockchain_block)\n\n"
            f"🔍 _Data obtained directly from the node._"
        ),
        color=0x5A9EC9
    )
    embed.set_thumbnail(url="https://raw.githubusercontent.com/ZentCashFoundation/brand/refs/heads/master/logo/stacked/zentcash_stacked_color.png")
    await ctx.send(embed=embed)

@commands.command(name="price")
async def price_command(ctx, pair: str = "ZTC_BTC"):

    base_url = "https://api.games.zent.cash:3000/api/exchange/market/ticker"
    api_url = f"{base_url}?pair={pair}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        result = data.get("result", {})

        last_price = result.get('last_price')
        ask_price = result.get('ask_price')
        bid_price = result.get('bid_price')
        spread = result.get('spread')

        try:
            last_price = float(last_price)
            ask_price = float(ask_price)
            bid_price = float(bid_price)
            spread = float(spread)
        except (TypeError, ValueError):
            last_price = ask_price = bid_price = spread = None

        if ask_price and ask_price != 0 and spread is not None:
            marginspread = (spread * 100) / ask_price
        else:
            marginspread = None

        pairformat1, pairformat2 = pair.split("_")

        if last_price is not None:
            message = (
                f"📊 **Price for {pairformat1}/{pairformat2}**\n\n"
                f"Last: {last_price:.12f}\n"
                f"Hight: {ask_price:.12f}\n"
                f"Low: {bid_price:.12f}\n"
                f"Spread: {spread:.12f}"
            )

            if marginspread is not None:
                message += f" ({marginspread:.2f}%)"

            message += "\n\n🔍 _Data obtained directly from the **Zent Cash Fun**._"

        else:
            message = f"⚠️ No data found for pair {pair.upper()}."

    except requests.exceptions.RequestException as e:
        message = f"⚠️ Error obtaining data: {e}"

    await ctx.send(message)


@commands.command(name="donate")
async def donate_command(ctx):
    embed = discord.Embed(
        title="Donate",
        description=(
            f" **BTC:** bc1qxzh342p9alru57gz29jexxlc90rdqzvzlvr6lz\n\n"
            f" **LTC:** ltc1qyaalrjd6qkg9805774hfwtrccwuencz8xeetcz\n\n"
            f" **DOGE:** D9M7Ef8G134iLeLP5cigvMNZ63gBZGAFJW\n\n"
	        f" **ETH:** 0xA16e6d3191B7EE5819Ea9d67e7d476f8881eB793\n\n"
	        f" **XUNI:** Xuniiirs6Vo8REdUmDf2vXM9PjnWZe6PfToy2sBkLCD1Hn5Dp2CN6G8JTpAMNUV5kB93zqi3GGv3SYPfok39xE7BJkSk74jUsBU\n\n"
            f" **XMR:** 42ooMsRFikjAJiB7yq4aRtBbtZMmNX3LuB9X8LFsD3edRnaCrvSSnG1b2f29SZggddSWMuuyLtNZZLFaYU3CYiSW6vVQq96\n\n"
            f" **XKR:** SEKReVwkp6DGx92JKtBT8yaBXR7iQmeWqcLBw8jcSWCTDShM8R5BZwLUveL917t47ohyFhj8NbG2QGAexqyAy3HkLPXP5kPxVXc\n\n"
            f" **ZTC:** Ze3iyuhaF8S3FxWgX3nqXodakwxqNzzgXgz4xGezWHPfRt3CsFDeV7EccVykYByuVeTnxTbwUh4CeBM21ftZKMn82QHzRSDe9\n\n"
        ),
        color=0x5A9EC9
    )
    embed.set_thumbnail(url="https://raw.githubusercontent.com/ZentCashFoundation/brand/refs/heads/master/logo/stacked/zentcash_stacked_color.png")
    await ctx.send(embed=embed)

# ------------------ Commands ------------------ #

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
bot.add_command(help_command)
bot.add_command(info_command)
bot.add_command(network_command)
bot.add_command(price_command)
bot.add_command(donate_command)
bot.run(BOT_TOKEN)
