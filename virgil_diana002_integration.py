"""
Integration file to register V.I.R.G.I.L / D.I.A.N.A_002 commands in OpenClaw.

Adds handlers for:
 /virgil
 /virgil_report
 /virgil_restart
 /virgil_cancel
"""

from virgil_diana002 import start_virgil_session, handle_virgil_text, show_virgil_report, restart_virgil_session, cancel_virgil_session

# Hypothetical OpenClaw command registration function
# Replace register_command with actual OpenClaw method

def register_commands(oc):
    @oc.command("virgil")
    def cmd_virgil(ctx):
        user_id = ctx.user.id
        
        response = start_virgil_session(user_id)
        return response

    @oc.command("virgil_report")
    def cmd_virgil_report(ctx):
        user_id = ctx.user.id
        return show_virgil_report(user_id)

    @oc.command("virgil_restart")
    def cmd_virgil_restart(ctx):
        user_id = ctx.user.id
        return restart_virgil_session(user_id)

    @oc.command("virgil_cancel")
    def cmd_virgil_cancel(ctx):
        user_id = ctx.user.id
        return cancel_virgil_session(user_id)

    @oc.on_message()
    def on_message(ctx):
        user_id = ctx.user.id
        text = ctx.text.strip() if ctx.text else ""

        # Only handle text if inside virgil session and not command
        if user_id in _workflows and not text.startswith("/"):
            # Route to workflow text handler
            return handle_virgil_text(user_id, text)

    print("V.I.R.G.I.L / D.I.A.N.A_002 commands registered.")

# To use, call register_commands(openclaw_instance)
