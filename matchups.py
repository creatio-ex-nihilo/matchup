'''
Author: creatio_ex_nihilo
Description: This is a short script to create a matchup table for some kind of event,
where any player from the previous round isn't allowed to participate, so basically
to have pauses for them.
Version: 0.1.2

DISCLAIMER: this script won't finish if your player count is < 5, because there
is no logically possible answer for that

let's look at an example
A, B, C, D
A:B
A:C
A:D
B:C
B:D
C:D

let's start with
A:D
the only possible next step is
B:C

the remaining steps are
A:B -> no, because B just had a turn
A:C -> no, because C just had a turn
B:D -> no, because B just had a turn
C:D -> no, because C just had a turn
'''
import random, math, string

class MatchupCreator:
    # constant copy dict
    match = {'player_1' : '', 'player_2' : '', 'already_taken' : 0}

    def __init__(self, players):
        self.players = list(set(players))
        self.matchups = self.create_matchups(self.players)

    def create_matchups(self, players):
        matchups = []
        for i in range(len(players)):
            current_player = players[i]
            for j in range(i+1,len(players)):
                tmp = [current_player, players[j]]
                random.shuffle(tmp)
                tmp_dict = MatchupCreator.match.copy()
                tmp_dict['player_1'] = tmp[0]
                tmp_dict['player_2'] = tmp[1]
                matchups.append(tmp_dict)
        return matchups

    def get_matchups(self):
        return self.matchups

    def sort_matchups(self, matchups):
        # constant
        loop_max = 5
        found_one = 0
        while found_one != 1:
            # (re)set 'already_taken'
            self.reset_taken_matchups(matchups)

            # offset
            random.shuffle(matchups)
            matchups[0]['already_taken'] = 1
            smus = [matchups[0]]
            current_matchup = smus[0]
            # init cnt
            cnt = self.get_nontaken_matchups_len(matchups)

            previous_cnt = cnt
            loop_cnt = 0
            while cnt != 0:
                if previous_cnt == cnt:
                    loop_cnt += 1
                elif previous_cnt != cnt:
                    loop_cnt = 0
                if loop_max < loop_cnt:
                    break

                for matchup in matchups:
                    if matchup['already_taken'] == 0 and self.cmp_matchups(current_matchup, matchup) == 1:
                        # choose matchup if none of the players participated in the previous one
                        matchup['already_taken'] = 1
                        smus.append(matchup)
                        current_matchup = smus[-1]
                        # update cnt
                        cnt = self.get_nontaken_matchups_len(matchups)
                        previous_cnt = cnt
            if cnt == 0:
                found_one = 1
        return smus

    def cmp_matchups(self, mu_1, mu_2):
        for player in mu_1.values():
            if player in mu_2.values():
                return 0
        return 1

    def reset_taken_matchups(self, matchups):
        for matchup in matchups:
            matchup['already_taken'] = 0

    def get_nontaken_matchups_len(self, matchups):
        cnt = 0
        for matchup in matchups:
            if matchup['already_taken'] == 0:
                cnt += 1
        return cnt

class MatchupTable:

    def __init__(self, players, matchups):
        self.players = list(set(players))
        self.matchups = matchups

    def print_matchup_plan(self):
        nr = 1
        lines = []
        max_len = self.calc_column_stuff()

        lines.append(self.create_column("-", [5, 1], '-') + self.create_column("-", max_len, '-') + self.create_column("-", [13, 5], '-') + self.create_column("-", max_len, '-') + '\n')
        lines.append(self.create_column("NR", [5, 1], ' ') + self.create_column("PLAYER1", max_len) + self.create_column("P1  :  P2", [13, 2]) + self.create_column("PLAYER2", max_len) + '\n')
        lines.append(self.create_column("-", [5, 1], '-') + self.create_column("-", max_len, '-') + self.create_column("-", [13, 5], '-') + self.create_column("-", max_len, '-') + '\n')
        for matchup in self.matchups:
            lines.append(self.create_column('{:03}'.format(nr), [5, 1], ' ') + self.create_column(matchup["player_1"], max_len) + self.create_column(":", [13, 6]) + self.create_column(matchup["player_2"], max_len) + '\n')
            lines.append(self.create_column("-", [5, 1], '-') + self.create_column("-", max_len, '-') + self.create_column("-", [13, 5], '-') + self.create_column("-", max_len, '-') + '\n')
            nr += 1
        return lines

    def print_table(self):
        player_list = sorted(self.players)
        max_len = self.calc_column_stuff()

        num_rows = 2 * (len(player_list) + 1)
        num_columns = (len(player_list) + 1)

        rows = []
        cnt_row = ""

        for i in range(num_rows):
            for j in range(num_columns):

                if i % 2 == 1:
                    if j == 0:
                        cnt_row += self.create_column("-", max_len, '-')
                    else:
                        if j == num_columns - 1:
                            cnt_row += self.create_column("-", [7, 1], '-')
                        else:
                            cnt_row += self.create_column("-", [9, 1], '-')
                else:
                    if j == 0 and i != 0:
                        # first column (except first row)
                        cnt_row += self.create_column(player_list[math.ceil(i/2 - 1)], max_len, ' ')
                        # cnt_row += create_column(player_list[i-1], max_len, ' ')
                    elif i == 0 and j != 0:
                        # first row (except first column)
                        if j == num_columns - 1:
                            cnt_row += self.create_column("COUNT", [7, 1], ' ')
                        else:
                            cnt_row += self.create_column('{}{:02}'.format("GAME ", j), [9, 1], ' ')
                    elif i == 0 and j == 0:
                        # first row first column
                        cnt_row += self.create_column("NAME", max_len, ' ')
                    else:
                        if j == num_columns - 1:
                            cnt_row += self.create_column(" ", [7, 1], ' ')
                        else:
                            cnt_row += self.create_column(" ", [9, 1], ' ')
            rows.append(cnt_row + '\n')
            cnt_row = ""
        return [rows[-1]] + rows

    def create_column(self, input, max_len, special_char = ' '):
        all_padding = max_len[0] - len(input)
        back_padding = all_padding - max_len[1]
        output = "|"
        for i in range(max_len[1]):
            output += special_char
        output += input
        for i in range(back_padding):
            output += special_char
        output += "|"
        return output

    def calc_column_stuff(self):
        # find the longest player name
        max_player_len = len(max(self.players, key=len))
        # yes, magic number, bad stuff, but it's just the length of "Player1"
        if max_player_len <= 7:
            max_player_len = 7
        # constant
        column_len = max_player_len + 2
        # filler offset
        offset = math.ceil((column_len - max_player_len) / 2)
        # returns the length of the widest column
        return [offset * 2 + max_player_len, offset]

class MatchupSave:

    def __init__(self, filename, table, matchup_plan):
        self.filename = filename
        self.table = table
        self.matchup_plan = matchup_plan

    def save(self):
        with open(self.filename + ".txt", 'w') as file:
            for line in self.matchup_plan:
                file.write(line)
            file.write('\n')
            for line2 in self.table:
                file.write(line2)

players = {"A"}

for i in range(1, 26):
    players.add(chr(65 + i))

c = MatchupCreator(players)
t = MatchupTable(players, c.sort_matchups(c.get_matchups()))
s = MatchupSave("test", t.print_table(), t.print_matchup_plan())

print(*t.print_matchup_plan())
print('\n')
print(*t.print_table())
#s.save()