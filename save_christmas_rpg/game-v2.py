import gradio as gr
import random

class Game:
    def __init__(self):
        self.state = {
            'found_sender': False,
            'santa_rescued': False,
            'team_members': [],
            'resources': [],
            'world_state': 'normal',
            'explored_library': False,
            'prepared_for_battle': False,
            'knowledge_from_whispers': False,
            'team_status': "none"  # Possible values: "none", "elf_scout", "reindeer", "both"
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
        # If Santa is already rescued
        if self.state['santa_rescued']:
            self.story = "You have already rescued Santa! Thanks for playing!"
            self.choices = "Type 'reset' to play again."
            return self.story, self.choices

        # Handle the current world state and choices
        if self.state['world_state'] == 'normal':
            # This is the initial scenario
            if '1' in player_choice:
                return self.ignore_letter()
            elif '2' in player_choice:
                return self.find_sender()
            elif '3' in player_choice:
                return self.prepare_supplies()
            elif 'reset' in player_choice.lower():
                return self.reset_game()
            else:
                self.choices = "Invalid choice. Type '1', '2', or '3'."
                return self.story, self.choices

        elif self.state['world_state'] == 'ominous':
            # After ignoring the letter, the player is now in the ominous scenario
            if '1' in player_choice:
                return self.investigate_whispers()
            elif '2' in player_choice:
                return self.prepare_rescue_mission()
            elif '3' in player_choice:
                return self.wait_and_see()
            elif 'reset' in player_choice.lower():
                return self.reset_game()
            else:
                self.choices = "Invalid choice. Type '1', '2', or '3'."
                return self.story, self.choices
        
        elif self.state['world_state'] == 'hesistant':
            # The player is hesistant
            if '1' in player_choice:
                return self.go_to_fortress()
            elif '2' in player_choice:
                return self.seek_allies_ominous()
            elif '3' in player_choice:
                return self.prepare_supplies()
            elif 'reset' in player_choice.lower():
                return self.reset_game()
            else:
                self.choices = "Invalid choice. Type '1', '2', or '3'."
                return self.story, self.choices
        
        elif self.state['world_state'] == 'well_read':
            # After investigating more at the library
            # Player now has more info and can choose next steps
            if '1' in player_choice:
                return self.go_to_fortress()
            elif '2' in player_choice:
                return self.prepare_supplies()
            elif '3' in player_choice:
                return self.study_book_again()
            elif 'reset' in player_choice.lower():
                return self.reset_game()
            else:
                self.choices = "Invalid choice. Type '1', '2', or '3'."
                return self.story, self.choices
        
        elif self.state['world_state'] == 'got_cloak':
            # You got a warm cloak
            if '1' in player_choice:
                return self.investigate_whispers()
            elif '2' in player_choice:
                return self.seek_final_allies()
            elif '3' in player_choice:
                return self.go_to_fortress()
            elif 'reset' in player_choice.lower():
                return self.reset_game()
            else:
                self.choices = "Invalid choice. Type '1', '2', or '3'."
                return self.story, self.choices

        elif self.state['world_state'] == 'informed':
            # After investigating whispers or preparing in ominous state
            # Player now has more info and can choose next steps
            if '1' in player_choice:
                return self.go_to_fortress()
            elif '2' in player_choice:
                return self.seek_allies_ominous()
            elif '3' in player_choice:
                return self.gather_more_supplies()
            elif 'reset' in player_choice.lower():
                return self.reset_game()
            else:
                self.choices = "Invalid choice. Type '1', '2', or '3'."
                return self.story, self.choices

        elif self.state['world_state'] == 'journey':
            # Once they are ready, heading to fortress triggers the final showdown
            if '1' in player_choice:
                return self.final_showdown()
            elif '2' in player_choice:
                return self.seek_final_allies()
            elif '3' in player_choice:
                return self.study_book_again()
            elif 'reset' in player_choice.lower():
                return self.reset_game()
            else:
                self.choices = "Invalid choice. Type '1', '2', or '3'."
                return self.story, self.choices

        else:
            # If we somehow end up in a state not handled, revert to initial logic
            if 'reset' in player_choice.lower():
                return self.reset_game()
            self.choices = "Something unexpected happened. Type 'reset' to start over."
            return self.story, self.choices
    
    def get_current_image(self):
        # Return different images depending on self.state['world_state'] or other conditions
        if self.state['santa_rescued']:
            return "images/victory.png"
        elif self.state['world_state'] == 'well_read':
            return "images/library.png"
        elif self.state['world_state'] == 'got_cloak':
            return "images/warm_cloak.png"
        elif self.state['world_state'] == 'elf_scout':
            return "images/elf.png"
        elif self.state['world_state'] == 'reindeer':
            return "images/reindeer.png"
        elif self.state['world_state'] == 'both_allies':
            return "images/both.png"
        elif self.state['world_state'] == 'journey':
            return "images/journey.png"
        elif self.state['world_state'] == 'informed':
            return "images/book-krampus.png"
        elif self.state['world_state'] in ['ominous', 'hesitant']:
            return "images/ominous-events.png"
        elif self.state['world_state'] == 'defeat':
            return "images/loss.png"
        else:
            # Normal initial state
            return "images/letter.png"


    def ignore_letter(self):
        self.state['world_state'] = 'ominous'
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
        self.state['world_state'] = 'informed'
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
        self.state['resources'].append("Warm Cloak")
        self.state['world_state'] = 'got_cloak'
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

    def investigate_whispers(self):
        self.state['knowledge_from_whispers'] = True
        self.state['world_state'] = 'informed'
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
        self.state['resources'].append("Rations")
        self.state['world_state'] = 'informed'
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
        self.state['world_state'] = 'hesistant'
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
        self.state['world_state'] = 'journey'
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
        self.state['team_members'].append("Elf Scout")

        # Update team status
        if self.state['team_status'] == "reindeer":
            self.state['team_status'] = "both"
            self.state['world_state'] = 'both_allies'
        else:
            self.state['team_status'] = "elf_scout"
            self.state['world_state'] = 'elf_scout'
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

    def gather_more_supplies(self):
        self.state['resources'].append("Healing Potion")
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

    def seek_final_allies(self):
        self.state['team_members'].append("Reindeer Warrior")

        # Update team status
        if self.state['team_status'] == "elf_scout":
            self.state['team_status'] = "both"
            self.state['world_state'] = 'both_allies'
        else:
            self.state['team_status'] = "reindeer"
            self.state['world_state'] = "reindeer"
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

    def study_book_again(self):
        self.state['explored_library'] = True
        self.state['world_state'] = 'well_read'
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

        # Increase victory chances based on team status
        if self.state['team_status'] == "both":
            outcome = "victory"  # Guaranteed victory if fully prepared and both allies recruited
        elif has_cloak and knows_clues and has_allies:
            outcome = "victory"
        elif has_cloak and knows_clues:
            outcome = random.choice(["victory", "victory", "defeat"])  # Higher chance of victory
        else:
            outcome = random.choice(["victory", "defeat"])

        if outcome == "victory":
            self.state['santa_rescued'] = True
            self.story = (
                "🎉 With your allies, supplies, and newfound knowledge, you breach Krampus's icy fortress. Using clever strategy and bravery, you defeat him in a fierce battle. "
                "As the dust settles, you free Santa from his chains. 🎅✨ Christmas is saved! The world rejoices, and you are hailed as a hero. 🌟🏆"
            )
            self.choices = "Type 'reset' to play again."
        else:
            self.state['world_state'] = 'defeat'
            self.story = (
                "💔 Despite your efforts, Krampus proves too strong. Without enough preparation, you find yourself overwhelmed. "
                "Santa remains captive, and an eternal winter descends upon the world. 🏔️❄️ But even in defeat, a spark of hope remains—perhaps you’ll try again. 🔄🌟"
            )
            self.choices = "Type 'reset' to try again."
        return self.story, self.choices


    def reset_game(self):
        self.__init__()
        return self.story, self.choices

# Initialize game instance
game_instance = Game()

def main(player_input):
    story, choices = game_instance.start_game(player_input)
    # Return empty string as the last output to clear input field
    image_path = game_instance.get_current_image()
    return story, choices, "", image_path

initial_story, initial_choices = game_instance.story, game_instance.choices
initial_image = game_instance.get_current_image()

with gr.Blocks() as interface:
    gr.Markdown("# Save Christmas RPG")
    gr.Markdown("Help rescue Santa Claus from Krampus! Type your choices to navigate the story. Use 'reset' to restart.")

    with gr.Row():  # Arrange everything in one row
        with gr.Column(scale=2):  # Left column
            # Move story and choices output above the input box
            story_output = gr.Textbox(label="Story Narrative", value=initial_story, lines=4)
            choices_output = gr.Textbox(label="Your Choices", value=initial_choices, lines=4)
            # Input box and submit button below
            input_box = gr.Textbox(label="Your Choice", placeholder="Enter '1', '2', or '3'")
            submit_button = gr.Button("Submit")
        with gr.Column(scale=1):  # Right column
            image_output = gr.Image(label="Current Scene", type="filepath", value=initial_image)

    submit_button.click(fn=main, inputs=input_box, outputs=[story_output, choices_output, input_box, image_output])


interface.launch(share=False, server_name="0.0.0.0", server_port=7860)
