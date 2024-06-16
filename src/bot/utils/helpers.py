import nextcord
from .users import UserManager

async def generate_key(interaction: nextcord.Interaction, reset: bool = False):
    await interaction.response.defer(ephemeral=True)

    check_key = await UserManager.get_user_by_id(interaction.user.id)

    if reset and not check_key:
        return await interaction.followup.send("You don't have an API key.", ephemeral=True)
    elif not reset and check_key:
        return await interaction.followup.send(f"Your API key is: {check_key['key']}", ephemeral=True)

    if reset:
        await UserManager.delete_key(interaction.user.id)

    generated_key = await UserManager.create_key(interaction.user.id)

    return await interaction.followup.send(f"Your new API key is: {generated_key}")

async def lookup(interaction: nextcord.Interaction, user: nextcord.Member = None):
    if not interaction.user.guild_permissions.manage_guild and user:
        return await interaction.send("You do not have permission to use this command to view other users.", ephemeral=True)

    await interaction.response.defer(ephemeral=True)

    check_key = await UserManager.get_user_by_id(interaction.user.id)

    if not check_key and not user:
        return await interaction.followup.send("You don't have an API key.")
    elif user and not check_key:
        return await interaction.followup.send(f"{user.mention} does not have an API key.")
    
    check_key.pop("_id", None)

    return await interaction.followup.send(f"Here is {user.mention if not user else 'your'} info: {check_key}")

async def switcher(interaction: nextcord.Interaction, user: nextcord.Member, banned: bool = None, premium: bool = None):
    if not interaction.user.guild_permissions.manage_guild and user:
        return await interaction.send("You do not have permission to use this command.", ephemeral=True)

    await interaction.response.defer(ephemeral=True)

    check_key = await UserManager.get_user_by_id(interaction.user.id)

    if not check_key:
        return await interaction.followup.send("This user does not have an API key.", ephemeral=True)
    
    if banned is not None:
        await UserManager.set_property(interaction.user.id, "banned", banned)
        return await interaction.followup.send(f"Successfully {'banned' if banned else 'unbanned'} {user.mention}.")
    elif premium is not None:
        await UserManager.set_property(interaction.user.id, "premium", premium)
        return await interaction.followup.send(f"Successfully {'gave' if premium else 'removed'} premium {'to' if premium else 'from'} {user.mention}.")