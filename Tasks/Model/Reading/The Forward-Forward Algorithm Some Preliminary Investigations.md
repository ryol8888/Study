
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
- 학습을 위해 forward pass에서 시행된 계산에 대한 완벽한 정보가 요구된다.
    ex. 블랙박스가 인풋으로 들어올경우 역전파 수행 X.
- 이 엣지 케이스에서 대안으로 강화학습을 사용할 순 있지만 높은 분산이 어려움을 겪게한다.
- 제안하는 알고리즘은 역전파와 속도가 비슷하지만 이 케이스에서 충분히 사용 가능함을 보여주었다. 멈추지 않고 신경망을 통해 순차 데이터를 굴리면서 학습 가능하다.

**2. The Forward-Forward Algorithm**
- 알고리즘의 아이디어는 forward-backward 방식 대신 forward-forward로 대신하는 것이다.
- positive forward with real data & negative forward with negative data
- goodness는 activation? object function. ex. sum of the squared.
- 여기선 goodness function = relu 레이어를 통과한 값들의 제곱의 합이라고 하자. 학습의 목적은 goodness function과 positive data가 특정 임계값보단 높아야되고 negative data가 임계값보다 낮아야된다.
  - goodness function을 저렇게 쓰는 이유. 1. 단순하다. 2. layer norm은 goodness의 모든 trace를 제거한다.
- 보다 구체적으로 로지스틱함수 $\sigma$를 적용하여 입력 벡터가 positive data일 떄 입렉 벡터를 올바르게 분류하는 것이다.
  $$
p(positivie) = \sigma (\Sigma_{j}{y^2_j - \theta})
  $$
- $y_i$는 layer noram을 하기 전 hidden unit $j$ 의 activity이다. 

**2.1 goodness function으로 mlp의 representation 학습하기.**
- 한 개의 layer로 goodness function을 이용하여 poistive/negative를 분류하는 것은 쉬운 것 처럼 보인다. 하지만 만약 첫 번재 히든 레이어의 activity가 두 번째 히든 레이어의 입력으로 활용되면 첫 번째 히든 레이어의 벡터 길이를 이용하여 negative data로부터 positive를 구별하는 것은 예측이 필요가 없는 수준이다. 이것을 예방하기 위하여 activity가 next layer의 입력으로 사용될 때 FF는 normalization을 진행한다. 이것은 첫 번째 레이어에서 분류를 위한 모든 정보를 없애버리는 효과를 가져오고 next 히든 레이어가 activity들의 상관관계 정보만을 가지고만 분류해야하는 상황을 강제한다. 이 상관관계는 layer norm을 통과한 이후에도 정보가 남아있다.바꿔 말하면 activity vector는 길이와 방향을 가지고 있다. 길이는 해당 레이어의 goodness를 정의하는 데 사용되며 방향만 다음 레이어로 전달된다.

3. Some experiments with FF
   - 이 논문은 FF 알고리즘에 대한 소개와 잘 작동하는지 작은 네트워크로 보여주는 것이고 다음 논문들이 큰 네트워크에서 얼마나 잘 작동하는지 보여줄 것이다.
3.1 baseline
   - 관습적으로 MNIST dataset을 이용하여 NN 알고리즘에 대한 테스트를 진행해왔다. 최근 설계된 CNN들은 일반적으로 0.6% test error를 갖는다.
   - 순열 불변 작업에서 신경망은 이미지의 spatial한 정보가 제공되지 않으므로 훈련 전에 무작위 순열에 따라 수행하면 동일하게 잘 수행된다.
   - 이 작업과 ReLU로 학습을 진행할 경우 일반적으로 1.4%의 test err가 나오는데 20 epoch이 걸린다.
   - 이는 drop out, label smoothing, supervised learning of label, unsupervised learning 등으로 1.1%까지 낮출 수 있다.
   - 요약하면 순열 불변 작업에선 복잡한 regularizer 없이 forward-backward와 비슷한 성능을 보여준다.
3.2 간단한 FF의 unsupervised 학습 예제
  - FF에서 대답해야될 두 가지 주요 질문이 있다.
  - 1. 우리가 좋은 negative data들을 가지고 있다면 데이터로부터 구조를 추출할 수 있는 multi-layer representation을 효율적으로 배울 수 있나?
    - 이 질문에 대한 답을 찾기 위해 hand-crafted 소스를 이용하여 조사를 시작했다.
    - 흔한 방법은 supervised learning에서 사용하는 contrastive learning을 사용하는 방법이다. 그 다음 간단한 linear transformation으로 represenatation vector를 조정하여 sfotmax로 결정하는 방법을 이용한다.  이것이 linear classification이다. 이것은 명백한 비선형임에도 선형 분류기라고 불린다.linear evaluation에서 하는 것처럼 FF도 이와같은 방식으로 표현 학습을 진행함에 사용될 수 있다. 
  - 2. negative data는 어디서 오나?
    - FF는 layer norm을 거치며 최대한 많은 correlation에 중점을 두기 위하여 positive와 매우 다른 긴 범위의 상관관계 정보와 매우 비슷한 짧은 범위의 상관관계를 갖는 negative data를 만들어야한다.
    - 만드는 방법은 random mask 이미지와 기존 이미지에 블러링( [1/4, 1/2, 1/4] )을 거친 이미지를 조합하여 만들었다. 임계값은 0.5로 설정.
    - 2000 ReLU & four hidden layer로 100 epoch동안 학습한 결과 test err 1.37%를 얻었다. 여기엔 추가적으로 마지막 세 개의 hidden layer에서 정규화된 벡터를 사용하였따. 
    - CNN을 사용하였으르 땐 1.16%의 테스트 error를 얻었다. hidden activity의 overfitting, underfitting을 방지하기 위해 peer norm을 사용했다.
3.3 간단한 FF의 supervised 학습 예제
    - unsupervised learning을 이용함으로써 얻는 이득들이 있지만 작은 모델, 하나의 Task만 필요로 한다면 supervised learning을 이용하는 것만으로도 충분하다. 이를 FF에 이용하는 방법은 입력에 label을 포함하는 것이다. positive data는 correct label을, negative data는 incorrect label를 포함시킨다. positive와 negative 데이터의 차이는 오직 label이기때문에 FF는 label에 상관관계가 없다면 image의 모든 feature를 무시할거다.
    - MNIST는 CNN의 학습을 쉽게하기 위해 black border를 가지고 있는데 만약 첫 10 pixel을 label을 표현한 vector로 놓으면 첫 hidden layer가 무엇을 배웠는지 보기 쉽다.