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
            'knowledge_from_whispers': False
        }
        self.story = "You receive a mysterious letter. Santa Claus has been kidnapped by Krampus! What will you do?"
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

        elif self.state['world_state'] == 'ready_for_fortress':
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
        elif self.state['world_state'] == 'ready_for_fortress':
            return "images/icy-fortress.png"
        elif self.state['world_state'] == 'informed':
            return "images/book-krampus.png"
        elif self.state['world_state'] == 'ominous':
            return "images/ominous-events.png"
        elif self.state['world_state'] == 'defeat':
            return "images/loss.png"
        else:
            # Normal initial state
            return "images/snowy-village.png"


    def ignore_letter(self):
        self.state['world_state'] = 'ominous'
        self.story = (
            "Ignoring the letter leads to ominous events: missing presents, a cold snap, "
            "and dread in the air. You hear whispers about Krampus's fortress."
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
        self.story = (
            "You head to the library and uncover Krampus's fortress location in the North Pole. "
            "You also find an ancient book with clues about defeating him."
        )
        self.choices = (
            "1. Head straight to the fortress\n"
            "2. Gather supplies and allies first\n"
            "3. Study the ancient book for more clues"
        )
        return self.story, self.choices

    def prepare_supplies(self):
        self.state['resources'].append("Warm Cloak")
        self.story = (
            "You spend time preparing supplies, gathering food, and crafting a Warm Cloak. "
            "The weather will no longer slow you down."
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
            "You follow the whispers into a dimly lit alleyway. An elf reveals intel on Krampus's guards, "
            "allowing you to slip past them more easily."
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
            "You gather a sturdy sled, some rations, and ensure your Warm Cloak is ready. "
            "You feel better prepared for what lies ahead."
        )
        self.choices = (
            "1. Head to Krampus's fortress\n"
            "2. Seek out allies in nearby villages\n"
            "3. Gather more supplies"
        )
        return self.story, self.choices

    def wait_and_see(self):
        self.state['world_state'] = 'informed'
        self.story = (
            "You wait, watching the sky grow darker. Strange silhouettes pass overhead. "
            "Tension builds, but now you have a better sense of the dangers ahead."
        )
        self.choices = (
            "1. Finally head to Krampus's fortress\n"
            "2. Seek allies to help you\n"
            "3. Gather more supplies before leaving"
        )
        return self.story, self.choices

    def go_to_fortress(self):
        self.state['world_state'] = 'ready_for_fortress'
        self.story = (
            "With the information gathered and some preparations made, you stand at the edge of "
            "Krampus's icy domain. The fortress looms in the distance."
        )
        self.choices = (
            "1. Attempt the final showdown\n"
            "2. Search for last-minute allies\n"
            "3. Study the ancient book one more time"
        )
        return self.story, self.choices

    def seek_allies_ominous(self):
        self.state['team_members'].append("Elf Scout")
        self.story = (
            "You travel to a small village and recruit an elf scout who knows secret paths "
            "and weaknesses in Krampus's guards."
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
            "You gather additional supplies: a Healing Potion and some warm gloves. "
            "With every preparation, you feel more confident."
        )
        self.choices = (
            "1. Head to Krampus's fortress\n"
            "2. Seek out allies now that you're well-supplied\n"
            "3. Study the ancient book before the journey"
        )
        return self.story, self.choices

    def seek_final_allies(self):
        self.state['team_members'].append("Reindeer Warrior")
        self.story = (
            "You find a Reindeer Warrior willing to join your cause. Strong and swift, "
            "this ally will give you an edge in battle."
        )
        self.choices = (
            "1. Attempt the final showdown now\n"
            "2. Gather more supplies\n"
            "3. Study the ancient book"
        )
        return self.story, self.choices

    def study_book_again(self):
        self.state['explored_library'] = True
        self.story = (
            "You revisit the ancient book, learning more about Krampus's weaknesses. "
            "This knowledge might turn the tide in your favor."
        )
        self.choices = (
            "1. Attempt the final showdown\n"
            "2. Seek out allies (if any left)\n"
            "3. Gather any last supplies"
        )
        return self.story, self.choices

    def final_showdown(self):
        # Determine outcome based on resources and knowledge
        has_cloak = "Warm Cloak" in self.state['resources']
        knows_clues = self.state['explored_library'] or self.state['knowledge_from_whispers']
        has_allies = len(self.state['team_members']) > 0

        # Increase chance of victory if player well-prepared
        if has_cloak and knows_clues and has_allies:
            outcome = "victory"
        elif has_cloak and knows_clues:
            outcome = random.choice(["victory", "victory", "defeat"])  # Higher chance of victory
        else:
            outcome = random.choice(["victory", "defeat"])

        if outcome == "victory":
            self.state['santa_rescued'] = True
            self.story = (
                "You arrive at Krampus's fortress, using your supplies and allies to breach the gates. "
                "Armed with knowledge from the ancient book, you outsmart Krampus and free Santa! "
                "Christmas is saved!"
            )
            self.choices = "Type 'reset' to play again."
        else:
            self.state['world_state'] = 'defeat'
            self.story = (
                "You face Krampus but are overwhelmed. Without sufficient preparation, "
                "the battle is lost. Santa remains captive, and winter consumes the world."
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
    # Arrange the input box, submit button, and image in a row with columns
    with gr.Row():
        with gr.Column(scale=2):
            input_box = gr.Textbox(label="Your Choice", placeholder="Enter '1', '2', or '3'")
            submit_button = gr.Button("Submit")
        with gr.Column(scale=1):
            # Set initial value to the starting image
            image_output = gr.Image(label="Current Scene", type="filepath", value=initial_image, width=400, height=400)

    story_output = gr.Textbox(label="Story Narrative", value=initial_story)
    choices_output = gr.Textbox(label="Your Choices", value=initial_choices)

    submit_button.click(fn=main, inputs=input_box, outputs=[story_output, choices_output, input_box, image_output])

interface.launch(share=False, server_name="0.0.0.0", server_port=7860)
