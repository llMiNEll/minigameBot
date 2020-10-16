import discord
import asyncio
import random
import pickle
from discord.ext import commands

client = commands.Bot(command_prefix=':G ')

fortune_point = [-6, -3, -1, 1, 4, 7, 10, 14, 19]
category = ["Aces", "Deuces", "Threes", "Fours", "Fives", "Sixes", "subtotal", "Choice", "4 of a Kind", "Full House",
            "S.Straight", "L.Straight", "Yacht", "Total"]


@client.event
async def on_ready():
    print("Bot ID : " + str(client.user.id))
    print("System Online")
    game = discord.Game("미니게임 준비")
    await client.change_presence(status=discord.Status.online, activity=game)


# score.bin 파일 불러오는 함수
def scoreFileRead(*user_name: discord.Member):
    try:
        with open("score.bin", "rb") as f:  # score 파일 읽기
            score_data = pickle.load(f)

    except FileNotFoundError:  # 파일이 없으면
        with open("score.bin", "wb+") as f:  # 파일을 만들기
            score_data = dict()
            pickle.dump(score_data, f)  # 저장

    for i in range(len(user_name)):
        if str(user_name[i].id) not in score_data:
            score_data[str(user_name[i].id)] = 0

    return score_data


# rsp.bin 파일 불러오는 함수
def rspFileRead(*user_name: discord.Member):
    try:
        with open("rsp.bin", "rb") as f:  # score 파일 읽기
            rsp_data = pickle.load(f)

    except FileNotFoundError:  # 파일이 없으면
        with open("rsp.bin", "wb+") as f:  # 파일을 만들기
            rsp_data = dict()
            pickle.dump(rsp_data, f)  # 저장

    for i in range(len(user_name)):
        if (str(user_name[i].id), "win") not in rsp_data:
            rsp_data[str(user_name[i].id), "win"] = 0
            rsp_data[str(user_name[i].id), "lose"] = 0
            rsp_data[str(user_name[i].id), "draw"] = 0

    return rsp_data


# fortune.bin 파일 불러오는 함수
def fortuneFileRead(*user_name: discord.Member):
    try:
        with open("fortune.bin", "rb") as f:  # score 파일 읽기
            fortune_data = pickle.load(f)

    except FileNotFoundError:  # 파일이 없으면
        with open("fortune.bin", "wb+") as f:  # 파일을 만들기
            fortune_data = dict()
            pickle.dump(fortune_data, f)  # 저장

    for i in range(len(user_name)):
        if (str(user_name[i].id), "7") not in fortune_data:
            fortune_data[str(user_name[i].id), "7"] = 0
            fortune_data[str(user_name[i].id), "8"] = 0
            fortune_data[str(user_name[i].id), "9"] = 0
            fortune_data[str(user_name[i].id), "Clear"] = 0

    return fortune_data


# yacht.bin 파일 불러오는 함수
def yachtFileRead(*user_name: discord.Member):
    try:
        with open("yacht.bin", "rb") as f:  # score 파일 읽기
            yacht_data = pickle.load(f)

    except FileNotFoundError:  # 파일이 없으면
        with open("yacht.bin", "wb+") as f:  # 파일을 만들기
            yacht_data = dict()
            pickle.dump(yacht_data, f)  # 저장

    for i in range(len(user_name)):
        if (str(user_name[i].id), "win") not in yacht_data:
            yacht_data[str(user_name[i].id), "win"] = 0
            yacht_data[str(user_name[i].id), "lose"] = 0
            yacht_data[str(user_name[i].id), "draw"] = 0
            yacht_data[str(user_name[i].id), "max"] = 0

    return yacht_data


@client.command(name="전적_검색", pass_context=True)
# No.100 점수 확인 명령
async def showName(ctx, user_name: discord.Member):
    score_data = scoreFileRead(user_name)
    rsp_data = rspFileRead(user_name)
    fortune_data = fortuneFileRead(user_name)
    yacht_data = yachtFileRead(user_name)

    # point
    embed = discord.Embed(title="[" + str(user_name) + "] Info", description=" ", color=0xffff00)
    embed.add_field(name="포인트", value=str(score_data[str(user_name.id)]) + " point", inline=False)
    # 가위바위보
    if rsp_data[str(user_name.id), "win"] == rsp_data[str(user_name.id), "lose"] == rsp_data[
        str(user_name.id), "draw"] == 0:
        embed.add_field(name="가위바위보", value="승률 : 0% [승무패 : 0 / 0 / 0]", inline=False)
    else:
        embed.add_field(name="가위바위보",
                        value="승률 : " + "{0:.3f}".format(100 * rsp_data[str(user_name.id), "win"] / (
                                rsp_data[str(user_name.id), "win"] + rsp_data[str(user_name.id), "lose"]))
                              + "% [승무패 : " + str(rsp_data[str(user_name.id), "win"]) + " / "
                              + str(rsp_data[str(user_name.id), "draw"]) + " / "
                              + str(rsp_data[str(user_name.id), "lose"]) + "]", inline=False)
    # 운빨망겜
    embed.add_field(name="운빨망겜", value="stage 7 : " + str(fortune_data[str(user_name.id), "7"])
                                       + "회 / stage 8 : " + str(fortune_data[str(user_name.id), "8"])
                                       + "회\nstage 9 : " + str(fortune_data[str(user_name.id), "9"])
                                       + "회 / All Stage Clear : " + str(
        fortune_data[str(user_name.id), "Clear"]) + "회", inline=False)
    # 야추
    if yacht_data[str(user_name.id), "win"] == yacht_data[str(user_name.id), "lose"] == yacht_data[
        str(user_name.id), "draw"] == 0:
        embed.add_field(name="야추",
                        value="승률 : 0% [승무패 : 0 / 0 / 0]\n최고 점수 : " + str(yacht_data[str(user_name.id), "max"]),
                        inline=False)
    else:
        embed.add_field(name="야추",
                        value="승률 : " + "{0:.3f}".format(100 * yacht_data[str(user_name.id), "win"] / (
                                yacht_data[str(user_name.id), "win"] + yacht_data[str(user_name.id), "lose"]))
                              + "% [승무패 : " + str(yacht_data[str(user_name.id), "win"]) + "/"
                              + str(yacht_data[str(user_name.id), "draw"]) + "/"
                              + str(yacht_data[str(user_name.id), "lose"])
                              + "]\n최고 점수 : " + str(yacht_data[str(user_name.id), "max"]), inline=False)
    await ctx.send(embed=embed)

    with open("score.bin", "wb") as f:
        pickle.dump(score_data, f)  # 저장하기
    with open("rsp.bin", "wb") as f:
        pickle.dump(rsp_data, f)
    with open("fortune.bin", "wb") as f:
        pickle.dump(fortune_data, f)
    with open("yacht.bin", "wb") as f:
        pickle.dump(yacht_data, f)


@client.command(name="가위바위보", pass_context=True)
# No.101 가위바위보 게임 명령
async def rsp(ctx):
    def rsp_text(num):
        if num == 0:
            return "가위"
        elif num == 1:
            return "바위"
        elif num == 2:
            return "보"

    score_data = scoreFileRead(ctx.author)
    rsp_data = rspFileRead(ctx.author)

    embed = discord.Embed(title="가위바위보 [Player : " + str(ctx.author) + "]",
                          description=":가위, :바위, :보 중 하나를 입력해 주세요.", color=0xaaaaaa)
    await ctx.send(embed=embed)

    while True:
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel  # 입력한 사람이 본인인지 확인

        msg = await client.wait_for("message", check=check)
        if msg.content == ":가위":
            user_choose = 0
            break
        elif msg.content == ":바위":
            user_choose = 1
            break
        elif msg.content == ":보":
            user_choose = 2
            break
        else:
            await ctx.send("잘못된 입력입니다. 다시 입력해주세요.")

    AI_choose = random.randint(0, 2)

    if user_choose == AI_choose:  # 비긴 경우
        rsp_data[str(ctx.author.id), "draw"] += 1
        embed = discord.Embed(title="Player : " + rsp_text(user_choose) + " vs. " + rsp_text(AI_choose) + " : Bot",
                              description="비겼습니다. 0 point 획득 [현재 point : " + str(score_data[str(ctx.author.id)]) + "]",
                              color=0xaaaaaa)

    elif user_choose - AI_choose == 1 or user_choose - AI_choose == -2:  # 이긴 경우
        score_data[str(ctx.author.id)] += 5
        rsp_data[str(ctx.author.id), "win"] += 1
        embed = discord.Embed(title="Player : " + rsp_text(user_choose) + " vs. " + rsp_text(AI_choose) + " : Bot",
                              description="이겼습니다! 5 point 획득 [현재 point : " + str(score_data[str(ctx.author.id)]) + "]",
                              color=0xaaaaaa)

    elif user_choose - AI_choose == -1 or user_choose - AI_choose == 2:  # 진 경우
        score_data[str(ctx.author.id)] -= 3
        if score_data[str(ctx.author.id)] < 0:
            score_data[str(ctx.author.id)] = 0
        rsp_data[str(ctx.author.id), "lose"] += 1
        embed = discord.Embed(title="Player : " + rsp_text(user_choose) + " vs. " + rsp_text(AI_choose) + " : Bot",
                              description="졌습니다. -3 point 획득 [현재 point : " + str(score_data[str(ctx.author.id)]) + "]",
                              color=0xaaaaaa)

    await ctx.send(embed=embed)

    with open("score.bin", "wb") as f:
        pickle.dump(score_data, f)  # 저장하기
    with open("rsp.bin", "wb") as f:
        pickle.dump(rsp_data, f)


@client.command(name="운빨망겜", pass_context=True)
# No.102 운빨망겜 명령
async def fortune(ctx):
    score_data = scoreFileRead(ctx.author)
    fortune_data = fortuneFileRead(ctx.author)

    embed = discord.Embed(title="운빨테스트 [Player : " + str(ctx.author) + "]",
                          description="게임 설명 : 1~10 중 아무 숫자나 하나를 입력하면 됩니다.", color=0x62d4a8)
    await ctx.send(embed=embed)

    global fortune_point
    stage = 1
    percent = 90
    get_point = fortune_point[0]
    num = [0 for p in range(10)]
    while True:
        embed = discord.Embed(title="운빨테스트 [Stage " + str(stage) + " / 확률 : " + str(percent) + ".0%]",
                              description=" ", color=0x62d4a8)
        await ctx.send(embed=embed)

        erase_two = 0
        while True:  # 숫자 입력 받기
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel  # 입력한 사람이 본인인지 확인

            try:
                msg = await client.wait_for("message", check=check)
                isRange = (1 <= int(msg.content) <= 10)

            except ValueError:
                erase_two += 1
                await ctx.channel.purge(limit=1)
                await ctx.send("잘못된 입력입니다. 1~10 사이의 정수를 입력해주세요.")

            else:
                if isRange:
                    break
                else:
                    erase_two += 1
                    await ctx.channel.purge(limit=1)
                    await ctx.send("잘못된 입력입니다. 1~10 사이의 정수를 입력해주세요.")

        i = 0  # 랜덤 뽑기
        for j in range(10):  # 값 초기화
            num[j] = False
        while i < (percent / 10):  # 랜덤 뽑기
            a = random.randint(0, 9)
            if not num[a]:
                i += 1
                num[a] = True

        if stage == 1:
            await ctx.channel.purge(limit=(2 + erase_two))
        else:
            await ctx.channel.purge(limit=(3 + erase_two))
        if num[int(msg.content) - 1]:  # 당첨인 경우
            if stage == 9:  # 마지막 스테이지까지 클리어 한 경우
                score_data[str(ctx.author.id)] += 25
                fortune_data[str(ctx.author.id), "Clear"] += 1
                embed = discord.Embed(title="마지막 9 stage 까지 클리어 했습니다! [Latest Stage : 어캐헀누!!]",
                                      description="27 point 획득 [현재 point : " + str(
                                          score_data[str(ctx.author.id)]) + "]", color=0x62d4a8)
                await ctx.send(embed=embed)

                with open("score.bin", "wb") as f:
                    pickle.dump(score_data, f)  # 저장하기
                break
            else:
                stage += 1
                percent -= 10
                get_point = fortune_point[stage - 1]
                embed = discord.Embed(title=str(msg.content) + "은(는) 꽝이 아니었습니다!", description=" ", color=0x62d4a8)
                await ctx.send(embed=embed)
        else:
            score_data[str(ctx.author.id)] += get_point
            if score_data[str(ctx.author.id)] < 0:
                score_data[str(ctx.author.id)] = 0
            if stage == 7:
                fortune_data[str(ctx.author.id), "7"] += 1
            if stage == 8:
                fortune_data[str(ctx.author.id), "8"] += 1
            if stage == 9:
                fortune_data[str(ctx.author.id), "9"] += 1

            p = 0
            clear_num: list = [0 for p in range(10 - stage)]
            for i in range(10):
                if num[i]:
                    clear_num[p] = i + 1
                    p += 1

            embed = discord.Embed(title=str(msg.content) + "은(는) 꽝입니다. [Latest Stage : " + str(stage) + "]",
                                  description=str(get_point) + " point 획득 [현재 point : " + str(
                                      score_data[str(ctx.author.id)]) + "]\n\n클리어 숫자 :", color=0x62d4a8)
            for i in range(10 - stage):
                embed.add_field(name="번호", value=str(clear_num[i]), inline=True)
            await ctx.send(embed=embed)

            with open("score.bin", "wb") as f:
                pickle.dump(score_data, f)  # 저장하기
            with open("fortune.bin", "wb") as f:
                pickle.dump(fortune_data, f)
            break


@client.command(name="야추", pass_context=True)
# No.103 Yacht 명령
async def yacht(ctx, opponent: discord.Member):
    score = [[0] * 2 for p in range(14)]
    cate = [[True] * 2 for p in range(14)]
    surren = [False, False]

    def check_ctx(m):  # player 입력 받는 조건 함수
        return m.author == ctx.author

    def check_opponent(m):  # opponent 입력 받는 조건 함수
        return m.author == opponent

    score_data = scoreFileRead(ctx.author, opponent)
    yacht_data = yachtFileRead(ctx.author, opponent)

    time_out = False
    start = False
    go = False

    if ctx.author == opponent:
        embed = discord.Embed(title="Yacht Dice [Single Play]",
                              description="Player A : [" + str(ctx.author) + "] vs. [" + str(opponent) + "] : Player B",
                              color=0x62d4a8)
        embed.add_field(name="[주의 사항]", value="1) 싱글 플레이에서는 승무패와 포인트가 저장되지 않습니다.\n"
                                              + "2) 텍스트가 나오자마자 채팅을 입력하면 오작동할 가능성이 있습니다.")
        await ctx.send(embed=embed)
        go = True
        await asyncio.sleep(3.0)
    else:
        embed = discord.Embed(title="Yacht Dice [2 Player]",
                              description="Player A : [" + str(ctx.author) + "] vs. [" + str(
                                  opponent) + "] : Player B\n"
                                          + str(opponent) + "님은 게임울 수락하려면 \"수락\"을, 아니면 \"거절\"을 입력하세요.", color=0x62d4a8)
        embed.add_field(name="[주의 사항]", value="1) 원활한 게임 진행을 위해 두 플레이어는 같은 체널을 사용해주세요.\n"
                                              + "2) 텍스트가 나오자마자 채팅을 입력하면 오작동할 가능성이 있습니다.")
        await ctx.send(embed=embed)

        while True:  # 상대방 입장 받기
            try:
                msg = await client.wait_for("message", check=check_opponent, timeout=15.0)
            except asyncio.TimeoutError:
                time_out = True
                break
            else:
                if msg.content == "수락":
                    start = True
                    break
                elif msg.content == "거절":
                    start = False
                    break
                else:
                    await ctx.send("잘못된 입력입니다. 다시 입력해주세요.")

        if time_out:  # 시간이 초과된 경우
            embed = discord.Embed(title="Yacht Dice [2 Player]",
                                  description="Player A : " + str(ctx.author) + " vs. " + str(
                                      opponent) + " : Player B\n"
                                              + "입력 시간이 초과되었습니다.", color=0x62d4a8)
            await ctx.send(embed=embed)

        elif not start:  # 게임이 거절된 경우
            embed = discord.Embed(title="Yacht Dice [2 Player]",
                                  description="Player A : " + str(ctx.author) + " vs. " + str(
                                      opponent) + " : Player B\n"
                                              + str(opponent) + "에 의해 게임이 거절되었습니다.", color=0x62d4a8)
            await ctx.send(embed=embed)

        else:  # 게임을 수락한 경우
            go = True

    if go:  # 게임이 수락된 경우
        for turn in range(24):
            fixed = [False, False, False, False, False]
            dice = [0 for p in range(5)]
            erase_two = 0

            if turn % 2 == 0:
                embed = discord.Embed(title="Yacht Dice [Player A's Turn (" + str(int(turn / 2) + 1) + " / 12)]",
                                      description="Player A : [" + str(ctx.author) + "] vs. [" + str(
                                          opponent) + "] : Player B", color=0xaa0000)
            else:
                embed = discord.Embed(title="Yacht Dice [Player B's Turn (" + str(int(turn / 2) + 1) + " / 12)]",
                                      description="Player A : [" + str(ctx.author) + "] vs. [" + str(
                                          opponent) + "] : Player B", color=0x0000aa)
            for i in range(len(category)):
                if i == 6:
                    if cate[i][turn % 2]:
                        embed.add_field(name=str(category[i]),
                                        value=str(score[i][0]) + " / " + str(
                                            score[i][1]) + " [Aces ~ Sixes가 63점 이상이면 보너스 35점]", inline=False)
                elif i == 13:
                    embed.add_field(name=str(category[i]),
                                    value=str(score[i][0]) + " / " + str(score[i][1]), inline=True)
                else:
                    if cate[i][turn % 2]:
                        embed.add_field(name="[" + str(i + 1) + ".] " + str(category[i]),
                                        value=str(score[i][0]) + " / " + str(score[i][1]), inline=True)
                    else:
                        embed.add_field(name=str(i + 1) + ". " + str(category[i]),
                                        value=str(score[i][0]) + " / " + str(score[i][1]), inline=True)
            embed.add_field(name="----------------------------------------------------------",
                            value="\"roll\"을 입력해서 주사위를 던지세요.\n게임을 그만두려면 \"항복\"을 입력하세요.", inline=False)
            await ctx.send(embed=embed)
            # 주사위 굴리기
            for p in range(3):
                def text(fix):
                    if fix:
                        return "x "
                    else:
                        return "o "

                if p != 0:
                    if turn % 2 == 0:
                        embed = discord.Embed(title="현재 주사위 [Player A]", color=0xaa0000)
                    else:
                        embed = discord.Embed(title="현재 주사위 [Player B]", color=0x0000aa)
                    embed.add_field(name="----------------------------------------------------------",
                                    value=str(dice[0]) + " " + str(dice[1]) + " " + str(dice[2]) + " " + str(
                                        dice[3]) + " " + str(dice[4])
                                          + "\n" + text(fixed[0]) + " " + text(fixed[1]) + " " + text(
                                        fixed[2]) + " " + text(fixed[3]) + " " + text(fixed[4]), inline=False)
                    await ctx.send(embed=embed)

                erase_two = 0
                while True:  # Player 입력받기 [roll]
                    if turn % 2 == 0:
                        msg = await client.wait_for("message", check=check_ctx)
                    else:
                        msg = await client.wait_for("message", check=check_opponent)
                    if msg.content == "roll":
                        break
                    elif msg.content == "항복":
                        if turn % 2 == 0:  # Player A가 항복한 경우
                            embed = discord.Embed(title="[Player A]", description="정말로 항복하시겠습니까?\n [yes] / [no]",
                                                  color=0xaa0000)
                        else:
                            embed = discord.Embed(title="[Player B]", description="정말로 항복하시겠습니까?\n [yes] / [no]",
                                                  color=0x0000aa)
                        await ctx.send(embed=embed)

                        while True:  # Player 입력받기
                            if turn % 2 == 0:
                                msg = await client.wait_for("message", check=check_ctx)
                            else:
                                msg = await client.wait_for("message", check=check_opponent)

                            if msg.content == "yes":
                                surren[turn % 2] = True
                                await ctx.channel.purge(limit=(4 + erase_two))
                                break
                            elif msg.content == "no":
                                await ctx.channel.purge(limit=(3 + erase_two))
                                erase_two = 0
                                break
                            else:
                                await ctx.channel.purge(limit=1)
                                erase_two += 1
                                await ctx.send("잘못된 입력입니다. 다시 입력해주세요.")
                        if msg.content == "yes":
                            break
                    else:
                        await ctx.channel.purge(limit=1)
                        erase_two += 1
                        await ctx.send("잘못된 입력입니다. 다시 입력해주세요.")

                if True in surren:
                    break

                for i in range(5):  # 주사위 굴리기
                    if not fixed[i]:
                        dice[i] = random.randint(1, 6)

                if p == 2:  # 마지막 차례는 고정 선택이 아니라 바로 점수 선택으로 건너뛰기
                    break

                if p == 0:
                    await ctx.channel.purge(limit=(1 + erase_two))
                else:
                    await ctx.channel.purge(limit=(2 + erase_two))
                if turn % 2 == 0:
                    embed = discord.Embed(title="현재 주사위 [Player A]", color=0xaa0000)
                else:
                    embed = discord.Embed(title="현재 주사위 [Player B]", color=0x0000aa)
                embed.add_field(name="----------------------------------------------------------",
                                value=str(dice[0]) + " " + str(dice[1]) + " " + str(dice[2]) + " " + str(
                                    dice[3]) + " " + str(dice[4])
                                      + "\n" + text(fixed[0]) + " " + text(fixed[1]) + " " + text(
                                    fixed[2]) + " " + text(fixed[3]) + " " + text(fixed[4])
                                      + "\n[다시 굴릴 주사위는 o, 고정할 주사위는 x로 입력해주세요. ex) x x o o x]", inline=False)
                await ctx.send(embed=embed)

                # 고정할 주사위 선택하는 부분
                erase_two = 0
                while True:
                    error = False
                    if turn % 2 == 0:
                        msg = await client.wait_for("message", check=check_ctx)
                    else:
                        msg = await client.wait_for("message", check=check_opponent)
                    param = msg.content.split()
                    if len(param) == 5:
                        for i in range(5):
                            if param[i] == "x":
                                fixed[i] = True
                            elif param[i] == "o":
                                fixed[i] = False
                            else:
                                error = True
                    else:
                        error = True

                    if not error:
                        break
                    else:
                        if msg.content == "항복":
                            if turn % 2 == 0:  # Player A가 항복한 경우
                                embed = discord.Embed(title="[Player A]", description="정말로 항복하시겠습니까?\n [yes] / [no]",
                                                      color=0xaa0000)
                            else:
                                embed = discord.Embed(title="[Player B]", description="정말로 항복하시겠습니까?\n [yes] / [no]",
                                                      color=0x0000aa)
                            await ctx.send(embed=embed)

                            while True:  # Player 입력받기
                                if turn % 2 == 0:
                                    msg = await client.wait_for("message", check=check_ctx)
                                else:
                                    msg = await client.wait_for("message", check=check_opponent)

                                if msg.content == "yes":
                                    surren[turn % 2] = True
                                    await ctx.channel.purge(limit=(4 + erase_two))
                                    break
                                elif msg.content == "no":
                                    await ctx.channel.purge(limit=(3 + erase_two))
                                    erase_two = 0
                                    break
                                else:
                                    await ctx.channel.purge(limit=1)
                                    erase_two += 1
                                    await ctx.send("잘못된 입력입니다. 다시 입력해주세요.")
                            if msg.content == "yes":
                                break
                        else:
                            erase_two += 1
                            await ctx.channel.purge(limit=1)
                            await ctx.send("잘못된 입력입니다. 다시 입력해주세요.")

                if True in surren:
                    break
                # 고정이 다 O 인 경우 반복 종료하고 점수 배정으로 넘어가기
                skip = 0
                for i in range(5):
                    if fixed[i]:
                        skip += 1
                if skip == 5:
                    break

                await ctx.channel.purge(limit=(2 + erase_two))
            # 점수 배정 하기
            if True in surren:
                break

            await ctx.channel.purge(limit=(2 + erase_two))
            if turn % 2 == 0:
                embed = discord.Embed(title="주사위 현황 [Player A]", color=0xaa0000)
            else:
                embed = discord.Embed(title="주사위 현황 [Player B]", color=0x0000aa)
            embed.add_field(name="----------------------------------------------------------",
                            value=str(dice[0]) + " " + str(dice[1]) + " " + str(dice[2]) + " " + str(
                                dice[3]) + " " + str(dice[4])
                                  + "\n[점수를 배정할 카테고리의 번호를 입력하세요.]", inline=False)
            await ctx.send(embed=embed)

            erase_two = 0
            while True:  # Player 입력받기 [카테고리]
                error = False
                choice = 0
                if turn % 2 == 0:
                    msg = await client.wait_for("message", check=check_ctx)
                else:
                    msg = await client.wait_for("message", check=check_opponent)

                if msg.content == "항복":
                    if turn % 2 == 0:  # Player A가 항복한 경우
                        embed = discord.Embed(title="[Player A]", description="정말로 항복하시겠습니까?\n [yes] / [no]",
                                              color=0xaa0000)
                    else:
                        embed = discord.Embed(title="[Player B]", description="정말로 항복하시겠습니까?\n [yes] / [no]",
                                              color=0x0000aa)
                    await ctx.send(embed=embed)

                    while True:  # Player 입력받기
                        if turn % 2 == 0:
                            msg = await client.wait_for("message", check=check_ctx)
                        else:
                            msg = await client.wait_for("message", check=check_opponent)

                        if msg.content == "yes":
                            surren[turn % 2] = True
                            await ctx.channel.purge(limit=(4 + erase_two))
                            break
                        elif msg.content == "no":
                            await ctx.channel.purge(limit=(3 + erase_two))
                            erase_two = 0
                            break
                        else:
                            await ctx.channel.purge(limit=1)
                            erase_two += 1
                            await ctx.send("잘못된 입력입니다. 다시 입력해주세요.")
                    if msg.content == "yes":
                        break
                else:
                    for i in range(14):
                        if msg.content == str(i + 1):
                            if cate[i][turn % 2]:
                                choice = i
                                cate[i][turn % 2] = False
                                break
                            else:
                                choice = 0
                                await ctx.channel.purge(limit=1)
                                erase_two += 1
                                await ctx.send("이미 할당된 카테고리입니다. 다른 카테고리를 입력해주세요.")
                                error = True
                                break

                    # subtotal / total
                    if choice == 6 or choice == 13:
                        await ctx.channel.purge(limit=1)
                        erase_two += 1
                        await ctx.send("subtotal이나 Total은 선택할 수 없습니다.")
                        error = True

                    # count 정의
                    count = [0 for p in range(6)]
                    for i in range(5):
                        count[dice[i] - 1] += 1

                    # Aces ~ Sixes
                    if 0 <= choice <= 5:
                        for i in range(6):
                            if choice == i:
                                for j in range(5):
                                    if dice[j] == (i + 1):
                                        score[i][turn % 2] += (i + 1)
                                cate[i][turn % 2] = False
                                break

                    # Choice
                    elif choice == 7:
                        for i in range(5):
                            score[7][turn % 2] += dice[i]
                        cate[7][turn % 2] = False

                    # 4 of a Kind
                    elif choice == 8:
                        for i in range(6):
                            if count[i] >= 4:
                                for j in range(5):
                                    score[8][turn % 2] += dice[j]
                                cate[8][turn % 2] = False
                                break
                    # Full House
                    elif choice == 9:
                        for i in range(36):
                            if count[int(i / 6)] == 3 and count[i % 6] == 2:
                                for j in range(5):
                                    score[9][turn % 2] += dice[j]
                                cate[9][turn % 2] = False
                                break
                    # S.Straight
                    elif choice == 10:
                        if count[2] >= 1 and count[3] >= 1:
                            if (count[0] >= 1 and count[1] >= 1) or (count[1] >= 1 and count[4] >= 1) or (
                                    count[4] >= 1 and count[5] >= 1):
                                score[10][turn % 2] = 15
                                cate[10][turn % 2] = False
                    # L.Straight
                    elif choice == 11:
                        if count[1] == 1 and count[2] == 1 and count[3] == 1 and count[4] == 1 and (
                                count[0] == 1 or count[5] == 1):
                            score[11][turn % 2] = 30
                            cate[11][turn % 2] = False
                    # Yacht
                    elif choice == 12:
                        for i in range(6):
                            if count[i] == 5:
                                score[12][turn % 2] = 50
                                cate[12][turn % 2] = False
                                break
                    else:
                        await ctx.channel.purge(limit=1)
                        erase_two += 1
                        await ctx.send("해당 번호는 존재하지 않습니다. 점수판에 옆의 번호로 입력해주세요.")
                        error = True

                    if not error:
                        await ctx.channel.purge(limit=(3 + erase_two))
                        break

            if True in surren:
                break

            # subtotal 계산
            score[6][turn % 2] = 0
            for j in range(6):
                score[6][turn % 2] += score[j][turn % 2]

            # bonus 점수
            if score[6][turn % 2] >= 63:
                bonus = 35
            else:
                bonus = 0

            # total 계산
            score[13][turn % 2] = 0
            for j in range(6, 13):
                score[13][turn % 2] += score[j][turn % 2]
            score[13][turn % 2] += bonus

        # 마무리 텍스트 출력
        embed = discord.Embed(title="Yacht Dice",
                              description="Player A : [" + str(ctx.author) + "] vs. [" + str(opponent)
                                          + "] : Player B", color=0xaaaaaa)
        for i in range(len(category)):
            if i == 6:
                embed.add_field(name="[" + str(category[i]) + "]", value=str(score[i][0]) + " / "
                                                                         + str(
                    score[i][1]) + " [Aces ~ Sixes가 63점 이상이면 보너스 35점]", inline=False)
            else:
                embed.add_field(name="[" + str(category[i]) + "]", value=str(score[i][0]) + " / "
                                                                         + str(score[i][1]), inline=True)
        await ctx.send(embed=embed)

        # 점수 계산 함수
        def scorefunc(player, outcome):
            get_point = 0
            if 150 <= score[13][player] < 200:
                get_point = 2
            elif 200 <= score[13][player] < 250:
                get_point = 4
            elif 250 <= score[13][player] < 275:
                get_point = 7
            elif 275 <= score[13][player] < 300:
                get_point = 10
            elif 300 <= score[13][player] <= 325:
                get_point = 15

            if outcome == "win":
                get_point += 15
            elif outcome == "lose":
                get_point -= 15

            return get_point

        # 점수 계산
        if ctx.author != opponent:
            if score[13][0] > score[13][1] or surren[1]:  # A가 이긴 경우
                score_data[str(ctx.author.id)] += scorefunc(0, "win")
                yacht_data[str(ctx.author.id), "win"] += 1
                score_data[str(opponent.id)] += scorefunc(1, "lose")
                yacht_data[str(opponent.id), "lose"] += 1

                embed = discord.Embed(title="Yacht Dice [" + str(ctx.author) + " 승리!!]", color=0xaa0000)
                embed.add_field(name="Player A : " + str(score[13][0]) + " vs. " + str(score[13][1]) + " : Player B"
                                , value="Player A : " + str(scorefunc(0, "win")) + " point 획득\n"
                                        + "[현재 point : " + str(score_data[str(ctx.author.id)]) + "]\n"
                                        + "Player B : " + str(scorefunc(1, "lose")) + " point 획득"
                                        + "[현재 point : " + str(score_data[str(opponent.id)]) + "]", inline=False)

            elif score[13][0] < score[13][1] or surren[0]:  # B가 이긴 경우
                score_data[str(ctx.author.id)] += scorefunc(0, "lose")
                yacht_data[str(ctx.author.id), "lose"] += 1
                score_data[str(opponent.id)] += scorefunc(1, "win")
                yacht_data[str(opponent.id), "win"] += 1

                embed = discord.Embed(title="Yacht Dice [" + str(opponent) + " 승리!!]", color=0x0000aa)
                embed.add_field(name="Player A : " + str(score[13][0]) + " vs. " + str(score[13][1]) + " : Player B"
                                , value="Player A : " + str(scorefunc(0, "lose")) + " point 획득"
                                        + "[현재 point : " + str(score_data[str(ctx.author.id)]) + "]\n"
                                        + "Player B : " + str(scorefunc(1, "win")) + " point 획득"
                                        + "[현재 point : " + str(score_data[str(opponent.id)]) + "]", inline=False)

            elif score[13][0] == score[13][1]:  # 무승부
                score_data[str(ctx.author.id)] += scorefunc(0, "draw")
                yacht_data[str(ctx.author.id), "draw"] += 1
                score_data[str(opponent.id)] += scorefunc(1, "draw")
                yacht_data[str(opponent.id), "draw"] += 1

                embed = discord.Embed(title="Yacht Dice [무승부입니다. (어캐했누)]", color=0xaaaaaa)
                embed.add_field(name="Player A : " + str(score[13][0]) + " vs. " + str(score[13][1]) + " : Player B"
                                , value="Player A : " + str(scorefunc(0, "draw")) + " point 획득"
                                        + " [현재 point : " + str(score_data[str(ctx.author.id)]) + "]\n"
                                        + "Player B : " + str(scorefunc(1, "draw")) + " point 획득"
                                        + " [현재 point : " + str(score_data[str(opponent.id)]) + "]", inline=False)

        else:
            embed = discord.Embed(title="Yacht Dice [Single Play]", color=0xaa0000)
            embed.add_field(name="Player A : " + str(score[13][0]) + " vs. " + str(score[13][1]) + " : Player B"
                            , value="Player A : " + str(scorefunc(0, "win")) + " point 획득\n"
                                    + "[Single Play는 최고 기록만 저장됩니다.", inline=False)

        await ctx.send(embed=embed)

        if score[13][0] > yacht_data[str(ctx.author.id), "max"]:
            yacht_data[str(ctx.author.id), "max"] = score[13][0]
        if score[13][1] > yacht_data[str(opponent.id), "max"]:
            yacht_data[str(opponent.id), "max"] = score[13][1]

        with open("score.bin", "wb") as f:  # 저장하기
            pickle.dump(score_data, f)
        with open("yacht.bin", "wb") as f:
            pickle.dump(yacht_data, f)


@client.command(name="점수_조정", pass_context=True)
# No.104 점수 추가 명령
async def change(ctx, type, user_name: discord.Member, amount):
    if ctx.author.id == 540360394691313664:  # 명령 입력한 사람이 llMiNEll인 경우
        check = False
        score_data = scoreFileRead(user_name)
        rsp_data = rspFileRead(user_name)
        fortune_data = fortuneFileRead(user_name)
        yacht_data = yachtFileRead(user_name)

        if type == "점수":
            score_data[str(user_name.id)] += int(amount)
            check = True

        elif type == "가위바위보:win":
            rsp_data[str(user_name.id), "win"] += int(amount)
            check = True

        elif type == "가위바위보:lose":
            rsp_data[str(user_name.id), "lose"] += int(amount)
            check = True

        elif type == "가위바위보:draw":
            rsp_data[str(user_name.id), "draw"] += int(amount)
            check = True

        elif type == "운빨망겜:7":
            fortune_data[str(user_name.id), "7"] += int(amount)
            check = True

        elif type == "운빨망겜:8":
            fortune_data[str(user_name.id), "8"] += int(amount)
            check = True

        elif type == "운빨망겜:9":
            fortune_data[str(user_name.id), "9"] += int(amount)
            check = True

        elif type == "운빨망겜:Clear":
            fortune_data[str(user_name.id), "Clear"] += int(amount)
            check = True

        elif type == "야추:win":
            yacht_data[str(user_name.id), "win"] += int(amount)
            check = True

        elif type == "야추:lose":
            yacht_data[str(user_name.id), "lose"] += int(amount)
            check = True

        elif type == "야추:draw":
            yacht_data[str(user_name.id), "draw"] += int(amount)
            check = True

        elif type == "야추:max":
            yacht_data[str(user_name.id), "max"] += int(amount)
            check = True

        if check:
            embed = discord.Embed(title="[System] \"" + type + "\"",
                                  description=str(user_name) + "의 점수가 " + amount + "만큼 증가하였습니다.", color=0xaaaaaa)
        else:
            embed = discord.Embed(title="[System] 점수 조정",
                                  description="Error 104002 : 존재하지 않는 type입니다.", color=0xaaaaaa)
        await ctx.send(embed=embed)

        with open("score.bin", "wb") as f:
            pickle.dump(score_data, f)  # 저장하기
        with open("rsp.bin", "wb") as f:
            pickle.dump(rsp_data, f)
        with open("fortune.bin", "wb") as f:
            pickle.dump(fortune_data, f)
        with open("yacht.bin", "wb") as f:
            pickle.dump(yacht_data, f)

    else:
        embed = discord.Embed(title="[System] 점수 조정", description="Error 104001 : 이 Bot의 소유자에게만 권한이 있습니다.",
                              color=0xaaaaaa)
        await ctx.send(embed=embed)

# 가위바위보 무승부 시 재대결

# 반응속도 테스트 wait_for 안쓰고 메세지 입력받기 (wait_for("message") 할 때 message에 관련된 내용 참고하면 될 듯

# 야추 일정 point 이상 사용 가능 기능 고려 + 최적화 + 야추 숫자입력 try ... expect 으로 바꾸기

# parameter 생략된 경우 에러창 띄우는 함수 만들기

client.run("NzYzMDAwMzc0MjM1NjI3NTIx.X3xVeQ.RMyxd55-Q_E3MQBMsK7HSRak4Bw")
