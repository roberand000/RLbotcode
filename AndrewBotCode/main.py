# This is the main file where you control your bot's strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits

# Hi! Corbin here. Note the line below says GoslingUtils in the videos.
# DO NOT change the line below. It's no longer compatible with GoslingUtils so we renamed it.
# There are a few places like this where the code that you started with (the code you downloaded) might
# look different than the videos. THAT'S OK! Don't change it. We've made it better over time.
# Just follow along with the videos and it will all work the same.
class Bot(BotCommandAgent):
    # This function runs every in-game tick (every time the game updates anything)
    def run(self):
        if self.intent is not None:
            return
        
        # set_intent tells the bot what it's trying to do
        if self.kickoff_flag:
            self.set_intent(kickoff())
            return
        if self.is_in_front_of_ball():
            self.set_intent(goto(self.friend_goal.location))
            return
        self.set_intent(short_shot(self.foe_goal.location))
        targets = {
            'at_opponent_goal':(self.foe_goal.left_post,self.foe_goal.right_post),
            'away_from_our_net':(self.friend_goal.right_post, self.friend_goal.left_post)
        }
        hits = find_hits(self,targets)
        if len(hits['at_opponent_goal']) > 0:
            self.set_intent(hits['at_opponent_goal'][0])
            print('at their goal')
            return
        if len (hits['away_from_our_net']) > 0:
            print('away from our goal')
            self.set_intent(hits['away_from_our_net'][0])
            return
        
        if self.me.boost > 99:
            self.set_intent(short_shot(self.foe_goal.location))
            return
        
        
        closest_boost = self.get_closest_large_boost()


        if closest_boost is not None:
            self.set_intent(goto(closest_boost.location)) 
            print('4')
            return
        
    
        if self.me.boost < 20 and self.is_not_in_front_of_ball():
            self.set_intent(goto(closest_boost.location))
            print('5')
            return
        
        if self.is_opponent_threatening():
            self.set_intent(goto(self.friend_goal.location))
            print('1')
            return

        if self.ball.location.z > 300 and self.me.boost > 30:
            self.set_intent(aerial_shot(self.ball.location, self.time + 1.5, self.foe_goal.location - self.ball.location, 0.9))
            print('3')
            return


    


