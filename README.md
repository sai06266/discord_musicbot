# Music_Bot

## Index
- Introduction
- 사용 방법 및 예시
- 그 외

## Introduction
평소에 여러명의 친구들과 게임을 하거나 대화를 나눌때, 디스코드라는 앱을 많이 이용했습니다. 디스코드를 이용하면서 여러 봇들의 존재 및 기능에 대해 알 수 있었고, 그 중에서도 음악을 재생해주는 봇을 많이 이용했습니다. 하지만 디스코드 음악봇들을 이용할 때 오류를 겪는 일이 종종 있었습니다. 이에 친구들이 장난으로 컴퓨터공학과인 저에게 오류없는 봇을 만들어달라는 이야기를 많이 했고, 저도 궁금하다는 생각이 들었습니다. 이번 기회에 수업시간에 배운 파이썬을 이용하여 디스코드 봇을 구현해보면서 디스코드 봇의 구현 방법 및 구조에 대한 궁금증을 풀어보고자 프로젝트를 진행하게 되었습니다.  
 
간단하게 구현 설명을 하자면 크롬드라이버로 사용자가 입력한 노래 제목을 유튜브에서 입력하여 검색한 후에 youtube_dl을 이용하여 노래를 재생하는 구조입니다.


## 사용 방법 및 예시

- 우선 봇을 디스코드 서버에 추가해야합니다.
  - [추가 링크](https://discord.com/api/oauth2/authorize?client_id=1039881426256007208&permissions=8&scope=bot)
  
  <img src = "/img/link.PNG" style = "width:250px" >
  
  - 원하는 서버를 선택하고 승인하여 봇을 서버에 추가할 수 있습니다.

 - 서버에 추가 후 코드를 실행시키면 다음과 같이 온라인 상태가 됩니다.
    
    <img src = "/img/online.PNG" style = "width:250px">
 <hr>   
 
 - 명령어를 이용하여 디스코드 봇을 이용하면 됩니다
    - 명령어 목록  
    
    <img src = "/img/command.PNG" style = "width:400px">
 <hr>
 
 #### <미니게임>
 간단한 미니게임 2가지를 만들었습니다. - 주사위 게임, 사다리타기
 - 주사위 게임(명령어: !주사위) : 봇과 사용자가 주사위 게임을 하여 결과를 출력합니다.
 
   <img src = "/img/dice.PNG" style = "width:250px">
  
 - 사다리타기 게임(명령어: !사다리[입력]/[결과]) : 사다리타기 게임을 진행하여 결과를 출력합니다.
 
   <img src = "/img/ladder.PNG" style = "width:250px">
   
 <hr>
 
 #### <음악>
 - 노래 재생(!play [노래제목])  
    - 명령어로 입력하면 봇이 음성채널로 입장해 음악을 재생합니다.  
    - 현재 노래가 재생 중이라면 재생목록에 추가합니다.  
   <img src = "/img/play.PNG" style = "width:400px">
 - 현재 노래(!now)  
    - 현재 재생중인 노래를 보여줍니다.  
   <img src = "/img/now.PNG" style = "width:400px">
 - 노래 정지(!pause), 재개(!resume), 스킵(!skip)  
    - 각 명령어로 노래를 정지, 재개, 스킵할 수 있습니다.  
    - 스킵했을 때 재생목록에 남아있는 노래가 없으면 봇은 음성채널을 떠납니다.  
   <img src = "/img/play2.PNG" style = "width:400px">
 - 재생목록 확인(!list), 재생 목록 초기화(!reset)  
    - 현재 재생목록을 보여줍니다.  
    - reset을 하면 재생목록의 내용이 사라집니다.  
   <img src = "/img/list.PNG" style = "width:400px">
 
 
 ## 그 외
 
 > 사용한 패키지 목록
 - discord
 - discord.ext
 - random
 - youtube_dl
 - selenium
 - bs4
 
 > 참고자료
 - [티스토리 파이프마임](https://seong6496.tistory.com/330)
    - 크롤링할 때 chrome-driver에 오류가 발생해 chrome-driver를 설치없이 바로 사용할 수 있게해 오류를 해결했습니다.
 - [티스토리](https://lektion-von-erfolglosigkeit.tistory.com/96)
    - 음악 재생을 구현할 때 참고했습니다.
 - License - MIT
