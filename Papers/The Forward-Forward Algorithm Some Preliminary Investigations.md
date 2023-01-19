
**Abstract**
이 논문은 새로운 NN 학습에 대해서 소개하려고 한다. 조금의 문제는 있지만 충분히 추가 연구를 할만하다.
Forward-forward 알고리즘은 두 개의 forward pass로 이루어지는데 하나는 positive data(real)와 negative data(generated with network itself)로 구성된다. 각 레이어마다 목적함수가 존재하며 positive data엔 high goodness, negative data엔 low goodness를 가진다. 레이어에서 제곱의 합은 goodness로 사용될 수 있지만 다른 어떤 것으로도 대체 가능하다. 이 두 개의 pass가 시간 내에 분리될 수 있다면 negative pass는 offline에서 수행가능하며 이는 positive pass에서 학습을 더욱 쉽게 만들어준다.

Abstract을 읽고 느낀점.
1. negative data를 스스로 생성하는 방식은 네트워크(class)안에 존재하는가
2. goodness == object function ?
3. FF(Forward-forward)에선 학습을 어떻게 진행하는가?


**1. What is wrong with backpropagation ?**
- 지난 decade 동안 backward 학습 방법은 많은 파라미터, 데이터를 학습시키위해 SGD 방법의 효용성을 확립.
- 하지만 실제 visual system에서 학습을 위해(backward를 위해) gradient를 저장한다는 증거는 없다.
- 대신 두 영역에서 6개의 layer를 통과하는 loop를 형성한다.
- 특히나 시퀸스 데이터를 학습하기 위해 시간으로 backwards 하는 행위는 학습이 거의 불가능하다.
Backpropagation의 문제점.
