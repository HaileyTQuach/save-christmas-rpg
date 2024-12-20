import gradio as gr
import random
import os
from enum import Enum

# Define Enums for World States and Team Statuses
class WorldState(Enum):
    NORMAL = 'normal'
    OMNINOUS = 'ominous'
    HESITANT = 'hesitant'
    INFORMED = 'informed'
    GOT_CLOAK = 'got_cloak'
    WELL_PREPARED = 'well_prepared'  # New State
    WELL_READ = 'well_read'
    ELF_SCOUT = 'elf_scout'
    REINDEER = 'reindeer'
    BOTH_ALLIES = 'both_allies'
    BOTH_ALLIES_FINAL = 'both_allies_final'
    JOURNEY = 'journey'
    DEFEAT = 'defeat'
    VICTORY = 'victory'

class TeamStatus(Enum):
    NONE = "none"
    ELF_SCOUT = "elf_scout"
    REINDEER = "reindeer"
    BOTH = "both"

# Game Class Definition
class Game:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        self.state = {
            'found_sender': False,
            'santa_rescued': False,
            'team_members': [],
            'resources': [],
            'world_state': WorldState.NORMAL.value,
            'explored_library': False,
            'prepared_for_battle': False,
            'knowledge_from_whispers': False,
            'team_status': TeamStatus.NONE.value  # Possible values: "none", "elf_scout", "reindeer", "both"
        }
        self.story = (
            "📜 One snowy evening, you find a mysterious letter waiting for you. The parchment feels cold in your hands, and the ink glistens like frost. "
            "Breaking the seal, you read the chilling words: 🎅 'Santa Claus has been taken! The malevolent Krampus has him bound in his icy fortress. 🏰❄️ "
            "Christmas is in grave danger. 🌟 The world needs a hero. 🦸‍♀️🦸‍♂️ What will you do?'"
        )

        self.choices = (
            "1. Ignore the letter\n"
            "2. Investigate and find the sender\n"
            "3. Prepare supplies before starting your quest"
        )

    def start_game(self, player_choice):
        player_choice = player_choice.strip()
        print(f"Current State: {self.state['world_state']}, Player Choice: '{player_choice}'")

        # If Santa is already rescued
        if self.state['santa_rescued']:
            self.story = "🎉 You have already rescued Santa! Thanks for playing! 🎄✨"
            self.choices = "Type 'reset' to play again."
            return self.story, self.choices

        # Handle the current world state and choices
        current_state = self.state['world_state']
        if current_state == WorldState.NORMAL.value:
            return self.handle_normal_state(player_choice)
        elif current_state == WorldState.OMNINOUS.value:
            return self.handle_ominous_state(player_choice)
        elif current_state == WorldState.HESITANT.value:
            return self.handle_hesitant_state(player_choice)
        elif current_state == WorldState.INFORMED.value:
            return self.handle_informed_state(player_choice)
        elif current_state == WorldState.WELL_PREPARED.value:
            return self.handle_well_prepared_state(player_choice)  # New Handler
        elif current_state == WorldState.WELL_READ.value:
            return self.handle_well_read_state(player_choice)
        elif current_state in [WorldState.GOT_CLOAK.value]:
            return self.handle_got_cloak_state(player_choice)
        elif current_state in [WorldState.BOTH_ALLIES.value, WorldState.ELF_SCOUT.value]:
            return self.handle_allies_state(player_choice)
        elif current_state in [WorldState.BOTH_ALLIES_FINAL.value, WorldState.REINDEER.value]:
            return self.handle_final_allies_state(player_choice)
        elif current_state == WorldState.JOURNEY.value:
            return self.handle_journey_state(player_choice)
        elif current_state in [WorldState.DEFEAT.value, WorldState.VICTORY.value]:
            if player_choice.lower() == 'reset':
                return self.reset_game_output()
            else:
                self.choices = "Type 'reset' to start over."
                return self.story, self.choices
        else:
            # Unexpected state
            self.choices = "Something unexpected happened. Type 'reset' to start over."
            return self.story, self.choices

    # Handlers for Different States
    def handle_normal_state(self, player_choice):
        if player_choice == '1':
            return self.ignore_letter()
        elif player_choice == '2':
            return self.find_sender()
        elif player_choice == '3':
            return self.prepare_supplies()
        elif player_choice.lower() == 'reset':
            return self.reset_game_output()
        else:
            self.choices = "❌ Invalid choice. Please enter '1', '2', or '3'."
            return self.story, self.choices

    def handle_ominous_state(self, player_choice):
        if player_choice == '1':
            return self.investigate_whispers()
        elif player_choice == '2':
            return self.prepare_rescue_mission()
        elif player_choice == '3':
            return self.wait_and_see()
        elif player_choice.lower() == 'reset':
            return self.reset_game_output()
        else:
            self.choices = "❌ Invalid choice. Please enter '1', '2', or '3'."
            return self.story, self.choices

    def handle_hesitant_state(self, player_choice):
        if player_choice == '1':
            return self.go_to_fortress()
        elif player_choice == '2':
            return self.seek_allies_ominous()
        elif player_choice == '3':
            return self.prepare_supplies()
        elif player_choice.lower() == 'reset':
            return self.reset_game_output()
        else:
            self.choices = "❌ Invalid choice. Please enter '1', '2', or '3'."
            return self.story, self.choices

    def handle_informed_state(self, player_choice):
        if player_choice == '1':
            return self.go_to_fortress()
        elif player_choice == '2':
            return self.seek_allies_informed()
        elif player_choice == '3':
            return self.gather_more_supplies()
        elif player_choice.lower() == 'reset':
            return self.reset_game_output()
        else:
            self.choices = "❌ Invalid choice. Please enter '1', '2', or '3'."
            return self.story, self.choices

    def handle_well_prepared_state(self, player_choice):
        if player_choice == '1':
            return self.go_to_fortress()
        elif player_choice == '2':
            return self.seek_allies_well_prepared()
        elif player_choice == '3':
            return self.study_book_again()
        elif player_choice.lower() == 'reset':
            return self.reset_game_output()
        else:
            self.choices = "❌ Invalid choice. Please enter '1', '2', or '3'."
            return self.story, self.choices

    def handle_well_read_state(self, player_choice):
        if player_choice == '1':
            return self.go_to_fortress()
        elif player_choice == '2':
            return self.prepare_supplies()
        elif player_choice == '3':
            return self.study_book_again()
        elif player_choice.lower() == 'reset':
            return self.reset_game_output()
        else:
            self.choices = "❌ Invalid choice. Please enter '1', '2', or '3'."
            return self.story, self.choices

    def handle_got_cloak_state(self, player_choice):
        if player_choice == '1':
            return self.investigate_whispers()
        elif player_choice == '2':
            return self.seek_final_allies()
        elif player_choice == '3':
            return self.go_to_fortress()
        elif player_choice.lower() == 'reset':
            return self.reset_game_output()
        else:
            self.choices = "❌ Invalid choice. Please enter '1', '2', or '3'."
            return self.story, self.choices

    def handle_allies_state(self, player_choice):
        if player_choice == '1':
            return self.go_to_fortress()
        elif player_choice == '2':
            return self.gather_more_supplies()
        elif player_choice == '3':
            return self.study_book_again()
        elif player_choice.lower() == 'reset':
            return self.reset_game_output()
        else:
            self.choices = "❌ Invalid choice. Please enter '1', '2', or '3'."
            return self.story, self.choices

    def handle_final_allies_state(self, player_choice):
        if player_choice == '1':
            return self.final_showdown()
        elif player_choice == '2':
            return self.gather_more_supplies()
        elif player_choice == '3':
            return self.study_book_again()
        elif player_choice.lower() == 'reset':
            return self.reset_game_output()
        else:
            self.choices = "❌ Invalid choice. Please enter '1', '2', or '3'."
            return self.story, self.choices

    def handle_journey_state(self, player_choice):
        if player_choice == '1':
            return self.final_showdown()
        elif player_choice == '2':
            return self.seek_final_allies()
        elif player_choice == '3':
            return self.study_book_again()
        elif player_choice.lower() == 'reset':
            return self.reset_game_output()
        else:
            self.choices = "❌ Invalid choice. Please enter '1', '2', or '3'."
            return self.story, self.choices

    # Additional Handler for Well Prepared State
    def handle_well_prepared_state(self, player_choice):
        if player_choice == '1':
            return self.go_to_fortress()
        elif player_choice == '2':
            return self.seek_allies_well_prepared()
        elif player_choice == '3':
            return self.study_book_again()
        elif player_choice.lower() == 'reset':
            return self.reset_game_output()
        else:
            self.choices = "❌ Invalid choice. Please enter '1', '2', or '3'."
            return self.story, self.choices

    def reset_game_output(self):
        self.reset_game()
        return self.story, self.choices

    # Image Mapping Method
    def get_current_image(self):
        image_mapping = {
            WorldState.VICTORY.value: "images/victory.png",
            WorldState.WELL_READ.value: "images/library.png",
            WorldState.GOT_CLOAK.value: "images/warm_cloak.png",
            WorldState.WELL_PREPARED.value: "images/well_prepared.png",  # New Image
            WorldState.ELF_SCOUT.value: "images/elf.png",
            WorldState.REINDEER.value: "images/reindeer.png",
            WorldState.BOTH_ALLIES.value: "images/both.png",
            WorldState.JOURNEY.value: "images/journey.png",
            WorldState.INFORMED.value: "images/book-krampus.png",
            WorldState.OMNINOUS.value: "images/ominous-events.png",
            WorldState.HESITANT.value: "images/ominous-events.png",
            WorldState.DEFEAT.value: "images/loss.png",
            WorldState.BOTH_ALLIES_FINAL.value: "images/both.png"
        }
        # Default image
        default_image = "images/letter.png"
        image_path = image_mapping.get(self.state['world_state'], default_image)
        # Verify if image exists; if not, use default
        if not os.path.isfile(image_path):
            print(f"Image not found: {image_path}. Using default image.")
            image_path = default_image
        return image_path

    # Choice Methods
    def ignore_letter(self):
        self.state['world_state'] = WorldState.OMNINOUS.value
        self.story = (
            "🎄 You turn away from the letter, trying to forget its ominous message. But soon, strange things begin to happen: "
            "presents disappear, a freezing cold snap grips the town, and a sense of dread fills the air. 🌬️🎁 "
            "You hear whispers in the wind, calling out Krampus’s name... 🧙‍♂️"
        )

        self.choices = (
            "1. Investigate the whispers\n"
            "2. Prepare supplies for a rescue mission\n"
            "3. Wait and see what happens"
        )
        return self.story, self.choices

    def find_sender(self):
        self.state['found_sender'] = True
        self.state['explored_library'] = True
        self.state['world_state'] = WorldState.INFORMED.value
        self.story = (
            "📚 You set off to uncover the truth behind the letter. At the library, you comb through ancient texts and mysterious clues. "
            "After hours of research, you discover the location of Krampus's icy fortress deep in the North Pole. 🧊🏔️ "
            "Among the dusty shelves, you also find an ancient book filled with secrets that may help you defeat him. 📖✨"
        )

        self.choices = (
            "1. Head straight to the fortress\n"
            "2. Gather supplies and allies first\n"
            "3. Study the ancient book for more clues"
        )
        return self.story, self.choices

    def prepare_supplies(self):
        if "Warm Cloak" not in self.state['resources']:
            self.state['resources'].append("Warm Cloak")
        self.state['world_state'] = WorldState.GOT_CLOAK.value
        self.story = (
            "🧣 You spend time gathering everything you’ll need for the journey: food, a sturdy sled, and a Warm Cloak to protect you from the biting cold. ❄️❄️ "
            "With your supplies ready, you feel more confident about the adventure ahead. 🚶‍♂️🎒"
        )

        self.choices = (
            "1. Investigate the whispers about Krampus\n"
            "2. Search for allies like elves or reindeer\n"
            "3. Head to the North Pole immediately"
        )
        return self.story, self.choices

    def gather_more_supplies(self):
        if "Healing Potion" not in self.state['resources']:
            self.state['resources'].append("Healing Potion")
        self.state['world_state'] = WorldState.WELL_PREPARED.value  # Update State to Well Prepared
        self.story = (
            "🛍️ You gather additional supplies: a Healing Potion, sturdy gloves, and a map to guide you. 🧤✨ Each preparation makes you feel more confident. "
            "You know that every small step brings you closer to rescuing Santa. 🎅💪"
        )

        self.choices = (
            "1. Head to Krampus's fortress\n"
            "2. Seek out allies now that you're well-supplied\n"
            "3. Study the ancient book before the journey"
        )
        return self.story, self.choices

    def investigate_whispers(self):
        if not self.state['knowledge_from_whispers']:
            self.state['knowledge_from_whispers'] = True
        self.state['world_state'] = WorldState.INFORMED.value
        self.story = (
            "🕯️ Guided by the whispers in the wind, you venture into a dimly lit alleyway. There, an elf reveals critical intel about Krampus's guards. "
            "With this knowledge, you can slip past his defenses undetected. 🧝‍♂️⚔️ The shadows seem to whisper, 'Prepare yourself...' 🌌"
        )

        self.choices = (
            "1. Head to Krampus's fortress now\n"
            "2. Seek out more allies before confronting Krampus\n"
            "3. Gather more supplies before you leave"
        )
        return self.story, self.choices

    def prepare_rescue_mission(self):
        if "Rations" not in self.state['resources']:
            self.state['resources'].append("Rations")
        self.state['world_state'] = WorldState.INFORMED.value
        self.story = (
            "🚨 You carefully plan your rescue mission, gathering rations and reinforcing your gear. With every step, you feel better prepared to face "
            "whatever dangers lie ahead. 🛷🍎 As the snow falls heavier, you tighten your cloak and look toward the North Pole. 🏔️"
        )

        self.choices = (
            "1. Head to Krampus's fortress\n"
            "2. Seek out allies in nearby villages\n"
            "3. Gather more supplies"
        )
        return self.story, self.choices

    def wait_and_see(self):
        self.state['world_state'] = WorldState.HESITANT.value
        self.story = (
            "👀 You decide to wait and observe. The world around you grows darker, and strange silhouettes pass through the skies. 🌌🦇 "
            "A chill runs down your spine, but the tension gives you a clearer sense of the dangers ahead. ❄️⏳"
        )

        self.choices = (
            "1. Finally head to Krampus's fortress\n"
            "2. Seek allies to help you\n"
            "3. Gather more supplies before leaving"
        )
        return self.story, self.choices

    def go_to_fortress(self):
        self.state['world_state'] = WorldState.JOURNEY.value
        self.story = (
            "🏰 Standing at the edge of Krampus’s icy domain, you take a deep breath. The fortress looms in the distance, shrouded in mist and danger. "
            "Every step forward feels heavier, but your resolve strengthens. The final battle is near. ⚔️❄️"
        )

        self.choices = (
            "1. Attempt the final showdown\n"
            "2. Search for last-minute allies\n"
            "3. Study the ancient book one more time"
        )
        return self.story, self.choices

    def seek_allies_ominous(self):
        if "Elf Scout" not in self.state['team_members']:
            self.state['team_members'].append("Elf Scout")

        # Update team status
        if self.state['team_status'] == TeamStatus.REINDEER.value:
            self.state['team_status'] = TeamStatus.BOTH.value
            self.state['world_state'] = WorldState.BOTH_ALLIES.value
        else:
            self.state['team_status'] = TeamStatus.ELF_SCOUT.value
            self.state['world_state'] = WorldState.ELF_SCOUT.value
        self.story = (
            "🧝 In a nearby village, you find an elf scout willing to join your cause. They know secret paths and weaknesses in Krampus's defenses. "
            "With this ally by your side, your chances of success grow. 🌟🛡️ 'Let’s save Christmas together,' they say, determination in their eyes."
        )

        self.choices = (
            "1. Head to Krampus's fortress\n"
            "2. Gather even more supplies\n"
            "3. Consult the ancient book again"
        )
        return self.story, self.choices

    def seek_allies_informed(self):
        if "Elf Scout" not in self.state['team_members']:
            self.state['team_members'].append("Elf Scout")

        # Update team status
        if self.state['team_status'] == TeamStatus.REINDEER.value:
            self.state['team_status'] = TeamStatus.BOTH.value
            self.state['world_state'] = WorldState.BOTH_ALLIES.value
        else:
            self.state['team_status'] = TeamStatus.ELF_SCOUT.value
            self.state['world_state'] = WorldState.ELF_SCOUT.value
        self.story = (
            "🧝 In a nearby village, you find an elf scout willing to join your cause. They know secret paths and weaknesses in Krampus's defenses. "
            "With this ally by your side, your chances of success grow. 🌟🛡️ 'Let’s save Christmas together,' they say, determination in their eyes."
        )

        self.choices = (
            "1. Head to Krampus's fortress\n"
            "2. Gather even more supplies\n"
            "3. Consult the ancient book again"
        )
        return self.story, self.choices

    def seek_allies_well_prepared(self):
        if "Reindeer Warrior" not in self.state['team_members']:
            self.state['team_members'].append("Reindeer Warrior")

        # Update team status
        if self.state['team_status'] == TeamStatus.ELF_SCOUT.value:
            self.state['team_status'] = TeamStatus.BOTH.value
            self.state['world_state'] = WorldState.BOTH_ALLIES_FINAL.value
        else:
            self.state['team_status'] = TeamStatus.REINDEER.value
            self.state['world_state'] = WorldState.REINDEER.value
        self.story = (
            "🦌 Deep in the snowy forest, you encounter a Reindeer Warrior with antlers gleaming like ice and eyes full of determination. "
            "Strong, swift, and loyal, they pledge to join your quest. With their strength by your side, the odds of victory grow brighter. ⚔️❄️"
        )
        self.choices = (
            "1. Attempt the final showdown now\n"
            "2. Gather more supplies\n"
            "3. Study the ancient book"
        )
        return self.story, self.choices

    def gather_more_supplies(self):
        if "Healing Potion" not in self.state['resources']:
            self.state['resources'].append("Healing Potion")
        self.state['world_state'] = WorldState.WELL_PREPARED.value  # Update State to Well Prepared
        self.story = (
            "🛍️ You gather additional supplies: a Healing Potion, sturdy gloves, and a map to guide you. 🧤✨ Each preparation makes you feel more confident. "
            "You know that every small step brings you closer to rescuing Santa. 🎅💪"
        )

        self.choices = (
            "1. Head to Krampus's fortress\n"
            "2. Seek out allies now that you're well-supplied\n"
            "3. Study the ancient book before the journey"
        )
        return self.story, self.choices

    def study_book_again(self):
        self.state['explored_library'] = True
        self.state['world_state'] = WorldState.WELL_READ.value
        self.story = (
            "📖 You pore over the ancient book, its pages revealing secrets about Krampus's weaknesses. The knowledge fills you with hope. "
            "Armed with this insight, you feel ready to face the challenge ahead. 🌟⚔️"
        )

        self.choices = (
            "1. Attempt the final showdown\n"
            "2. Seek out allies (if any left)\n"
            "3. Gather any last supplies"
        )
        return self.story, self.choices

    def final_showdown(self):
        has_cloak = "Warm Cloak" in self.state['resources']
        knows_clues = self.state['explored_library'] or self.state['knowledge_from_whispers']
        has_allies = len(self.state['team_members']) > 0

        # Determine outcome based on preparation and allies
        if self.state['team_status'] == TeamStatus.BOTH.value:
            outcome = "victory"  # Guaranteed victory with both allies
        elif has_cloak and knows_clues and has_allies:
            outcome = "victory"
        elif has_cloak and knows_clues:
            outcome = random.choices(["victory", "victory", "defeat"], weights=[2, 2, 1], k=1)[0]
        else:
            outcome = random.choice(["victory", "defeat"])

        # Prepare lists of resources and allies
        resources = ", ".join(self.state['resources']) if self.state['resources'] else "None"
        allies = ", ".join(self.state['team_members']) if self.state['team_members'] else "None"

        if outcome == "victory":
            self.state['santa_rescued'] = True
            self.state['world_state'] = WorldState.VICTORY.value
            self.story = (
                f"🎉 With your allies ({allies}), supplies ({resources}), and newfound knowledge, you breach Krampus's icy fortress. "
                "Using clever strategy and bravery, you defeat him in a fierce battle. As the dust settles, you free Santa from his chains. 🎅✨ "
                "Christmas is saved! The world rejoices, and you are hailed as a hero. 🌟🏆"
            )
            self.choices = "Type 'reset' to play again."
        else:
            self.state['world_state'] = WorldState.DEFEAT.value
            self.story = (
                f"💔 Despite your efforts, Krampus proves too strong. Without enough preparation and support, you find yourself overwhelmed. "
                f"Santa remains captive, and an eternal winter descends upon the world. 🏔️❄️ But even in defeat, a spark of hope remains—perhaps you’ll try again. 🔄🌟\n\n"
                f"**Your Resources:** {resources}\n"
                f"**Your Allies:** {allies}"
            )
            self.choices = "Type 'reset' to try again."
        return self.story, self.choices

    # Additional Method to Seek Allies in Well Prepared State
    def seek_allies_well_prepared(self):
        if "Reindeer Warrior" not in self.state['team_members']:
            self.state['team_members'].append("Reindeer Warrior")

        # Update team status
        if self.state['team_status'] == TeamStatus.ELF_SCOUT.value:
            self.state['team_status'] = TeamStatus.BOTH.value
            self.state['world_state'] = WorldState.BOTH_ALLIES_FINAL.value
        else:
            self.state['team_status'] = TeamStatus.REINDEER.value
            self.state['world_state'] = WorldState.REINDEER.value
        self.story = (
            "🦌 Deep in the snowy forest, you encounter a Reindeer Warrior with antlers gleaming like ice and eyes full of determination. "
            "Strong, swift, and loyal, they pledge to join your quest. With their strength by your side, the odds of victory grow brighter. ⚔️❄️"
        )
        self.choices = (
            "1. Attempt the final showdown now\n"
            "2. Gather more supplies\n"
            "3. Study the ancient book"
        )
        return self.story, self.choices

    # Final Showdown Method (Already Updated Above)

# Initialize game instance
game_instance = Game()

# Main Function for Gradio Interface
def main(player_input):
    story, choices = game_instance.start_game(player_input)
    image_path = game_instance.get_current_image()
    # Return empty string to clear input field
    return story, choices, "", image_path

# Initial outputs
initial_story, initial_choices = game_instance.story, game_instance.choices
initial_image = game_instance.get_current_image()

# Gradio Interface
with gr.Blocks() as interface:
    gr.Markdown("# 🎄 Save Christmas RPG 🎅")
    gr.Markdown("Help rescue Santa Claus from Krampus! Type your choices to navigate the story. Use 'reset' to restart.")

    with gr.Row():
        with gr.Column(scale=2):
            # Story and choices
            story_output = gr.Textbox(
                label="📖 Story Narrative",
                value=initial_story,
                lines=10,
                interactive=False
            )
            choices_output = gr.Textbox(
                label="📝 Your Choices",
                value=initial_choices,
                lines=4,
                interactive=False
            )
            # Input and submit
            input_box = gr.Textbox(
                label="🔍 Your Choice",
                placeholder="Enter '1', '2', or '3'",
                lines=1
            )
            submit_button = gr.Button("➡️ Submit")
        with gr.Column(scale=1):
            image_output = gr.Image(
                label="🌄 Current Scene",
                type="filepath",
                value=initial_image
            )

    # Define what happens on button click
    submit_button.click(
        fn=main,
        inputs=input_box,
        outputs=[story_output, choices_output, input_box, image_output]
    )

# Launch the interface
interface.launch(share=False, server_name="0.0.0.0", server_port=7860)
