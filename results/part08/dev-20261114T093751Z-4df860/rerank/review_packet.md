# Dev agent review — rerank

Unfilled review labels are pending, not zero scores.

## d7-dev-q01

Khi các yếu tố khác không đổi, giá hàng hóa tăng thì lượng cầu thường thay đổi thế nào?

Status: answered

Expected answer/behavior: Lượng cầu giảm; đó là quan hệ nghịch giữa giá và lượng cầu.

Agent answer: Khi các yếu tố khác không đổi, giá hàng hóa tăng thì lượng cầu thường **giảm**. Tài liệu nêu rằng khi giá tăng thì lượng cầu giảm, và ngược lại; đây là **luật cầu** [8bbe33c027de7a644a572c3d].

Citation IDs: ["8bbe33c027de7a644a572c3d"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 4, "evidence": "Economists call this inverse relationship between price and quantity demanded the law of demand. The law of demand assumes that all other variables that affect demand (which we explain in the next module) are held constant."}]

Final context:

```text
[202195399cb73d530929cc3b | data/day6/economics-chapters-3-4.pdf | PDF page 23]
A change in production costs caused a change in supply for the Postal Service. Step 3. Was the effect on supply positive or negative? Higher labor compensation leads to a lower quantity supplied of postal services at every given price, causing the supply curve for postal services to shift to the left, from S0 to S1. Step 4. Compare the new equilibrium price and quantity to the original equilibrium price. The new equilibrium (E1) occurs at a lower quantity and a higher price than the original equilibrium (E0). Figure 3.18 (b) shows the shift in demand in the following steps. Step 1. Draw a demand and supply model to illustrate what the market for U.S. Postal Services looked like before this scenario starts. The demand curve D0 and the supply curve S0 show the original relationships. Note that this diagram is independent from the diagram in panel (a). Step 2. Did the change described affect supply or demand? 

[3e9cfa16dec452a1fc4487d0 | data/day6/economics-chapters-3-4.pdf | PDF page 18]
Notice that a change in the price of the product itself is not among the factors that shift the supply curve. Although a change in price of a good or service typically causes a change in quantity supplied or a movement along the supply curve for that specific good or service, it does not cause the supply curve itself to shift.

[8bbe33c027de7a644a572c3d | data/day6/economics-chapters-3-4.pdf | PDF page 5]
FIGURE 3.2 A Demand Curve for Gasoline The demand schedule shows that as price rises, quantity demanded decreases, and vice versa. We graph these points, and the line connecting them is the demand curve (D). The downward slope of the demand curve again illustrates the law of demand—the inverse relationship between prices and quantity demanded. Demand curves will appear somewhat different for each product. They may appear relatively steep or flat, or they may be straight or curved. Nearly all demand curves share the fundamental similarity that they slope down from left to right. Demand curves embody the law of demand: As the price increases, the quantity demanded decreases, and conversely, as the price decreases, the quantity demanded increases. Confused about these different types of demand? Read the next Clear It Up feature. Is demand the same as quantity demanded? In economic terminology, demand is not the same as quantity demanded. 

[9b3d98e18c2784d2d5315086 | data/day6/economics-chapters-3-4.pdf | PDF page 25]
A higher or lower price never shifts the supply curve, as suggested by the shift in supply from S1 to S2. Instead, a price change leads to a movement along a given supply curve. Similarly, a higher or lower price never shifts a demand curve, as suggested in the shift from D0 to D1. Instead, a price change leads to a movement along a given demand curve. Remember, a change in the price of a good never causes the demand or supply curve for that good to shift. Think carefully about the timeline of events: What happens first, what happens next? What is cause, what is effect? If you keep the order right, you are more likely to get the analysis correct. In the four-step analysis of how economic events affect equilibrium price and quantity, the movement from the old to the new equilibrium seems immediate. As a practical matter, however, prices and quantities often do not zoom straight to equilibrium. 

[f9fedf8cbf8a12709cba514d | data/day6/economics-chapters-3-4.pdf | PDF page 14]
When a demand curve shifts, it will then intersect with a given supply curve at a different equilibrium price and quantity. We are, however, getting ahead of our story. Before discussing how changes in demand can affect equilibrium price and quantity, we first need to discuss shifts in supply curves. How Production Costs Affect Supply A supply curve shows how quantity supplied will change as the price rises and falls, assuming ceteris paribus so that no other economically relevant factors are changing. If other factors relevant to supply do change, then the entire supply curve will shift. Just as we described a shift in demand as a change in the quantity demanded at every price, a shift in supply means a change in the quantity supplied at every price. In thinking about the factors that affect supply, remember what motivates firms: profits, which are the difference between revenues and costs. 
```

## d7-dev-q02

Quy luật cung mô tả quan hệ giữa giá và lượng cung như thế nào, với điều kiện gì?

Status: answered

Expected answer/behavior: Giá cao hơn đi cùng lượng cung cao hơn và ngược lại, khi các yếu tố khác ảnh hưởng cung không đổi.

Agent answer: Quy luật cung nói rằng giá và lượng cung có quan hệ cùng chiều: khi giá cao hơn thì lượng cung thường tăng, còn khi giá thấp hơn thì lượng cung thường giảm [33ff8c5898ad4c98954a6562]. Điều này được nêu trong bối cảnh đường cung có độ dốc dương, tức là “the law of supply says that a higher price typically leads to a higher quantity supplied” [0096f11a38f0b867733dae97].

Citation IDs: ["33ff8c5898ad4c98954a6562", "0096f11a38f0b867733dae97"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 5, "evidence": "Economists call this positive relationship between price and quantity supplied—that a higher price leads to a higher quantity supplied and a lower price leads to a lower quantity supplied—the law of supply. The law of supply assumes that all other variables that affect supply (to be explained in the next module) are held constant."}, {"source_id": "openstax-principles-economics-3e", "page": 33, "evidence": "law of supply the common relationship that a higher price leads to a greater quantity supplied and a lower price leads to a lower quantity supplied, while all other variables are held constant"}]

Final context:

```text
[d186b4cf738611e9f0bd60c1 | data/day6/economics-chapters-3-4.pdf | PDF page 33]
 combination of price and quantity where there is no economic pressure from surpluses or shortages that would cause price or quantity to change equilibrium price the price where quantity demanded is equal to quantity supplied equilibrium quantity the quantity at which quantity demanded and quantity supplied are equal for a certain price level excess demand at the existing price, the quantity demanded exceeds the quantity supplied; also called a shortage excess supply at the existing price, quantity supplied exceeds the quantity demanded; also called a surplus factors of production the resources such as labor, materials, and machinery that are used to produce goods and services; also called inputs inferior good a good in which the quantity demanded falls as income rises, and in which quantity demanded rises and income falls inputs the resources such as labor, materials, and machinery that are used to produce goods and services; also called factors of production law of demand the common

[0096f11a38f0b867733dae97 | data/day6/economics-chapters-3-4.pdf | PDF page 19]
Draw a demand and supply model before the economic change took place. To establish the model requires four standard pieces of information: The law of demand, which tells us the slope of the demand curve is negative; the law of supply, which tells us that the slope of the supply curve is positive; the shift variables for demand; and the shift variables for supply. From this model, find the initial equilibrium values for price and quantity. Step 2. Decide whether the economic change you are analyzing affects demand or supply. In other words, does the event refer to something in the list of demand factors or supply factors? Step 3. Decide whether the effect on demand or supply causes the curve to shift to the right or to the left, and sketch the new demand or supply curve on the diagram. In other words, does the event increase or decrease the amount consumers want to buy or producers want to sell? Step 4. 

[33ff8c5898ad4c98954a6562 | data/day6/economics-chapters-3-4.pdf | PDF page 34]
A demand curve shows the relationship between quantity demanded and price in a given market on a graph. The law of demand states that a higher price typically leads to a lower quantity demanded. A supply schedule is a table that shows the quantity supplied at different prices in the market. A supply curve shows the relationship between quantity supplied and price on a graph. The law of supply says that a higher price typically leads to a higher quantity supplied. The equilibrium price and equilibrium quantity occur where the supply and demand curves cross. The equilibrium occurs where the quantity demanded is equal to the quantity supplied. If the price is below the equilibrium level, then the quantity demanded will exceed the quantity supplied. Excess demand or a shortage will exist. If the price is above the equilibrium level, then the quantity supplied will exceed the quantity demanded. Excess supply or a surplus will exist. 

[95f22f31c535038b647592ca | data/day6/economics-chapters-3-4.pdf | PDF page 50]
(The opportunity set model that we introduced in the Choice in a World of Scarcity chapter was the first.) Just as it would be foolish to try to learn the arithmetic of long division by memorizing every possible combination of numbers that can be divided by each other, it would be foolish to try to memorize every specific example of demand and supply in this chapter, this textbook, or this course. Demand and supply is not primarily a list of examples. It is a model to analyze prices and quantities. Even though demand and supply diagrams have many labels, they are fundamentally the same in their logic. Your goal should be to understand the underlying model so you can use it to analyze any market. Figure 4.9 displays a generic demand and supply curve. The horizontal axis shows the different measures of quantity: a quantity of a good or service, or a quantity of labor for a given job, or a quantity of financial capital. 
```

## d7-dev-q03

Theo chương 3, cầu khác lượng cầu ở điểm nào?

Status: answered

Expected answer/behavior: Cầu là quan hệ trên cả đường cong; lượng cầu là một điểm cụ thể trên đường cong.

Agent answer: Theo chương 3, **cầu** là mối quan hệ giữa **giá cả** và **lượng cầu** tại mọi mức giá; còn **lượng cầu** là số lượng cụ thể được mua ở **một mức giá nhất định**. Sách cũng nhấn mạnh rằng khi **giá thay đổi** thì ta có **sự di chuyển dọc theo đường cầu**, tức là thay đổi **lượng cầu**, chứ không phải dịch chuyển đường cầu. [48cea9212e2e6a95f9628560]

Citation IDs: ["48cea9212e2e6a95f9628560"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 5, "evidence": "In short, demand refers to the curve and quantity demanded refers to a (specific) point on the curve."}]

Final context:

```text
[db193469cfd44181dc49a85d | data/day6/economics-chapters-3-4.pdf | PDF page 17]
(Desired profit is not necessarily the same as economic profit, which will be explained in Chapter 7.) If you add these two parts together, you get the price the firm wishes to charge. The quantity Q0 and associated price P0 give you one point on the firm’s supply curve, as Figure 3.12 illustrates. FIGURE 3.12 Setting Prices The cost of production and the desired profit equal the price a firm will set for a product. Step 3. Now, suppose that the cost of production increases. Perhaps cheese has become more expensive by $0.75 per pizza. If that is true, the firm will want to raise its price by the amount of the increase in cost ($0.75). Draw this point on the supply curve directly above the initial point on the curve, but $0.75 higher, as Figure 3.13 shows.

[cc374bf8ed83d6dc1a3305e6 | data/day6/economics-chapters-3-4.pdf | PDF page 21]
price is $3.25 per pound and the original equilibrium quantity is 250,000 fish. (This price per pound is what commercial buyers pay at the fishing docks. What consumers pay at the grocery is higher.) Step 2. Did the economic event affect supply or demand? Good weather is an example of a natural condition that affects supply. Step 3. Was the effect on supply an increase or a decrease? Good weather is a change in natural conditions that increases the quantity supplied at any given price. The supply curve shifts to the right, moving from the original supply curve S0 to the new supply curve S1, which Figure 3.16 and Table 3.6 show. Step 4. Compare the new equilibrium price and quantity to the original equilibrium. At the new equilibrium E1, the equilibrium price falls from $3.25 to $2.50, but the equilibrium quantity increases from 250,000 to 550,000 salmon. Notice that the equilibrium quantity demanded increased, even though the demand curve did not move. 

[202195399cb73d530929cc3b | data/day6/economics-chapters-3-4.pdf | PDF page 23]
A change in production costs caused a change in supply for the Postal Service. Step 3. Was the effect on supply positive or negative? Higher labor compensation leads to a lower quantity supplied of postal services at every given price, causing the supply curve for postal services to shift to the left, from S0 to S1. Step 4. Compare the new equilibrium price and quantity to the original equilibrium price. The new equilibrium (E1) occurs at a lower quantity and a higher price than the original equilibrium (E0). Figure 3.18 (b) shows the shift in demand in the following steps. Step 1. Draw a demand and supply model to illustrate what the market for U.S. Postal Services looked like before this scenario starts. The demand curve D0 and the supply curve S0 show the original relationships. Note that this diagram is independent from the diagram in panel (a). Step 2. Did the change described affect supply or demand? 

[dd3f7ff7265f53a27dee731e | data/day6/economics-chapters-3-4.pdf | PDF page 13]
Draw a dotted horizontal line from the chosen price, through the original quantity demanded, to the new point with the new Q1. Draw a dotted vertical line down to the horizontal axis and label the new Q1. Figure 3.7 provides an example. FIGURE 3.7 Demand Curve with Income Increase With an increase in income, consumers will purchase larger quantities, pushing demand to the right. Step 3. Now, shift the curve through the new point. You will see that an increase in income causes an upward (or rightward) shift in the demand curve, so that at any price the quantities demanded will be higher, as Figure 3.8 illustrates. WORK IT OUT

[48cea9212e2e6a95f9628560 | data/day6/economics-chapters-3-4.pdf | PDF page 25]
the shift from the original demand curve, D0 to D1 on the diagram (labeled Shift 3), and the equilibrium moves from E2 to E3.” FIGURE 3.20 Shifts of Demand or Supply versus Movements along a Demand or Supply Curve A shift in one curve never causes a shift in the other curve. Rather, a shift in one curve causes a movement along the second curve. At about this point, Lee suspects that this answer is headed down the wrong path. Think about what might be wrong with Lee’s logic, and then read the answer that follows. Answer: Lee’s first step is correct: that is, a drought shifts back the supply curve of wheat and leads to a prediction of a lower equilibrium quantity and a higher equilibrium price. This corresponds to a movement along the original demand curve (D0), from E0 to E1. The rest of Lee’s argument is wrong, because it mixes up shifts in supply with quantity supplied, and shifts in demand with quantity demanded. 
```

## d7-dev-q04

Trong ví dụ xăng, giá và lượng cân bằng là bao nhiêu?

Status: answered

Expected answer/behavior: Giá cân bằng 1,40 USD/gallon; lượng cân bằng 600 triệu gallon trong ví dụ.

Agent answer: Trong ví dụ xăng, giá cân bằng là 1,40 đô la mỗi gallon và lượng cân bằng là 600 triệu gallon [a82898c46ebd459e8b89c69c].

Citation IDs: ["a82898c46ebd459e8b89c69c"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 8, "evidence": "In Figure 3.4, the equilibrium price is $1.40 per gallon of gasoline and the equilibrium quantity is 600 million gallons."}]

Final context:

```text
[e4f9df118aebc21a28f406af | data/day6/economics-chapters-3-4.pdf | PDF page 8]
In Figure 3.4, the equilibrium price is $1.40 per gallon of gasoline and the equilibrium quantity is 600 million gallons. If you had only the demand and supply schedules, and not the graph, you could find the equilibrium by looking for the price level on the tables where the quantity demanded and the quantity supplied are equal. The word “equilibrium” means “balance.” If a market is at its equilibrium price and quantity, then it has no reason to move away from that point. However, if a market is not at equilibrium, then economic pressures arise to move the market toward the equilibrium price and the equilibrium quantity. Imagine, for example, that the price of a gallon of gasoline was above the equilibrium price—that is, instead of $1.40 per gallon, the price is $1.80 per gallon. The dashed horizontal line at the price of $1.80 in Figure 3.4 illustrates this above-equilibrium price. At this higher price, the quantity demanded drops from 600 to 500. 

[a82898c46ebd459e8b89c69c | data/day6/economics-chapters-3-4.pdf | PDF page 7]
Figure 3.4 illustrates the interaction of demand and supply in the market for gasoline. The demand curve (D) is identical to Figure 3.2. The supply curve (S) is identical to Figure 3.3. Table 3.3 contains the same information in tabular form. FIGURE 3.4 Demand and Supply for Gasoline The demand curve (D) and the supply curve (S) intersect at the equilibrium point E, with a price of $1.40 and a quantity of 600. The equilibrium price is the only price where quantity demanded is equal to quantity supplied. At a price above equilibrium like $1.80, quantity supplied exceeds the quantity demanded, so there is excess supply. At a price below equilibrium such as $1.20, quantity demanded exceeds quantity supplied, so there is excess demand. Price (per gallon) Quantity demanded (millions of gallons) Quantity supplied (millions of gallons) $1.00 800 500 $1.20 700 550 $1.40 600 600 TABLE 3.3 Price, Quantity Demanded, and Quantity Supplied

[d92f5d8faec20a03ef6d7db8 | data/day6/economics-chapters-3-4.pdf | PDF page 8]
However, the below-equilibrium price reduces gasoline producers’ incentives to produce and sell gasoline, and the quantity supplied falls from 600 to 550.

[65f6f9ff98dae2d7dc25d679 | data/day6/economics-chapters-3-4.pdf | PDF page 4]
license has no effective demand for a car. What a buyer pays for a unit of the specific good or service is called price. The total number of units that consumers would purchase at that price is called the quantity demanded. A rise in price of a good or service almost always decreases the quantity demanded of that good or service. Conversely, a fall in price will increase the quantity demanded. When the price of a gallon of gasoline increases, for example, people look for ways to reduce their consumption by combining several errands, commuting by carpool or mass transit, or taking weekend or vacation trips closer to home. Economists call this inverse relationship between price and quantity demanded the law of demand. The law of demand assumes that all other variables that affect demand (which we explain in the next module) are held constant. We can show an example from the market for gasoline in a table or a graph. 

[cc374bf8ed83d6dc1a3305e6 | data/day6/economics-chapters-3-4.pdf | PDF page 21]
price is $3.25 per pound and the original equilibrium quantity is 250,000 fish. (This price per pound is what commercial buyers pay at the fishing docks. What consumers pay at the grocery is higher.) Step 2. Did the economic event affect supply or demand? Good weather is an example of a natural condition that affects supply. Step 3. Was the effect on supply an increase or a decrease? Good weather is a change in natural conditions that increases the quantity supplied at any given price. The supply curve shifts to the right, moving from the original supply curve S0 to the new supply curve S1, which Figure 3.16 and Table 3.6 show. Step 4. Compare the new equilibrium price and quantity to the original equilibrium. At the new equilibrium E1, the equilibrium price falls from $3.25 to $2.50, but the equilibrium quantity increases from 250,000 to 550,000 salmon. Notice that the equilibrium quantity demanded increased, even though the demand curve did not move. 
```

## d7-dev-q05

Khi giá thấp hơn mức cân bằng, thị trường bị thiếu hụt hay dư thừa, vì sao?

Status: answered

Expected answer/behavior: Thiếu hụt vì lượng cầu vượt lượng cung.

Agent answer: Khi giá thấp hơn mức cân bằng, thị trường bị **thiếu hụt** (excess demand), không phải dư thừa. Lý do là ở mức giá thấp hơn, **lượng cầu vượt quá lượng cung**; giá thấp làm lượng cầu tăng lên trong khi lượng cung bị giảm xuống. [33ff8c5898ad4c98954a6562]

Citation IDs: ["33ff8c5898ad4c98954a6562"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 9, "evidence": "When the price is below equilibrium, there is excess demand, or a shortage—that is, at the given price the quantity demanded, which has been stimulated by the lower price, now exceeds the quantity supplied, which has been depressed by the lower price."}, {"source_id": "openstax-principles-economics-3e", "page": 33, "evidence": "excess demand at the existing price, the quantity demanded exceeds the quantity supplied; also called a shortage"}, {"source_id": "openstax-principles-economics-3e", "page": 34, "evidence": "If the price is below the equilibrium level, then the quantity demanded will exceed the quantity supplied. Excess demand or a shortage will exist."}]

Final context:

```text
[33ff8c5898ad4c98954a6562 | data/day6/economics-chapters-3-4.pdf | PDF page 34]
A demand curve shows the relationship between quantity demanded and price in a given market on a graph. The law of demand states that a higher price typically leads to a lower quantity demanded. A supply schedule is a table that shows the quantity supplied at different prices in the market. A supply curve shows the relationship between quantity supplied and price on a graph. The law of supply says that a higher price typically leads to a higher quantity supplied. The equilibrium price and equilibrium quantity occur where the supply and demand curves cross. The equilibrium occurs where the quantity demanded is equal to the quantity supplied. If the price is below the equilibrium level, then the quantity demanded will exceed the quantity supplied. Excess demand or a shortage will exist. If the price is above the equilibrium level, then the quantity supplied will exceed the quantity demanded. Excess supply or a surplus will exist. 

[fe3ade2d487b951b3cb47418 | data/day6/economics-chapters-3-4.pdf | PDF page 33]
 relationship that a higher price leads to a lower quantity demanded of a certain good or service and a lower price leads to a higher quantity demanded, while all other variables are held constant law of supply the common relationship that a higher price leads to a greater quantity supplied and a lower price leads to a lower quantity supplied, while all other variables are held constant normal good a good in which the quantity demanded rises as income rises, and in which quantity demanded falls as income falls price what a buyer pays for a unit of the specific good or service price ceiling a legal maximum price price control government laws to regulate prices instead of letting market forces determine prices price floor a legal minimum price producer surplus the extra benefit producers receive from selling a good or service, measured by the price the producer actually received minus the price the producer would have been willing to accept quantity demanded the total number of units of

[daeac1ee809e1c32bc4ed9d1 | data/day6/economics-chapters-3-4.pdf | PDF page 9]
When the price is below equilibrium, there is excess demand, or a shortage—that is, at the given price the quantity demanded, which has been stimulated by the lower price, now exceeds the quantity supplied, which has been depressed by the lower price. In this situation, eager gasoline buyers mob the gas stations, only to find many stations running short of fuel. Oil companies and gas stations recognize that they have an opportunity to make higher profits by selling what gasoline they have at a higher price. As a result, the price rises toward the equilibrium level. Read Demand, Supply, and Efficiency for more discussion on the importance of the demand and supply model. 

[1dfce7af16248593ff3dfedc | data/day6/economics-chapters-3-4.pdf | PDF page 8]
In this situation, some producers and sellers will want to cut prices, because it is better to sell at a lower price than not to sell at all. Once some sellers start cutting prices, others will follow to avoid losing sales. These price reductions in turn will stimulate a higher quantity demanded. Therefore, if the price is above the equilibrium level, incentives built into the structure of demand and supply will create pressures for the price to fall toward the equilibrium. Now suppose that the price is below its equilibrium level at $1.20 per gallon, as the dashed horizontal line at this price in Figure 3.4 shows. At this lower price, the quantity demanded increases from 600 to 700 as drivers take longer trips, spend more minutes warming up the car in the driveway in wintertime, stop sharing rides to work, and buy larger cars that get fewer miles to the gallon. 

[8051fa4df46528c7c8aa47a7 | data/day6/economics-chapters-3-4.pdf | PDF page 16]
Now, imagine that the price of steel, an important ingredient in manufacturing cars, rises, so that producing a car has become more expensive. At any given price for selling cars, car manufacturers will react by supplying a lower quantity. We can show this graphically as a leftward shift of supply, from S0 to S1, which indicates that at any given price, the quantity supplied decreases. In this example, at a price of $20,000, the quantity supplied decreases from 18 million on the original supply curve (S0) to 16.5 million on the supply curve S1, which is labeled as point L. Conversely, if the price of steel decreases, producing a car becomes less expensive. At any given price for selling cars, car manufacturers can now expect to earn higher profits, so they will supply a higher quantity. The shift of supply to the right, from S0 to S2, means that at all prices, the quantity supplied has increased. 
```

## d7-dev-q06

Giả định ceteris paribus có nghĩa là gì trong mô hình cung cầu?

Status: answered

Expected answer/behavior: Giữ các yếu tố liên quan khác không đổi khi phân tích tác động của yếu tố đang xét.

Agent answer: Giả định ceteris paribus nghĩa là “các yếu tố khác không đổi” hay “các yếu tố khác bằng nhau” khi phân tích cung hoặc cầu [b707422cb03dc81d2cab1d30]. Nói cách khác, khi xem xét tác động của một biến như giá, các yếu tố kinh tế liên quan khác được giữ nguyên để phân tích [4d3953793110140eb560f1fd].

Citation IDs: ["b707422cb03dc81d2cab1d30", "4d3953793110140eb560f1fd"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 9, "evidence": "Economists call this assumption ceteris paribus, a Latin phrase meaning “other things being equal.” Any given demand or supply curve is based on the ceteris paribus assumption that all else is held equal."}, {"source_id": "openstax-principles-economics-3e", "page": 34, "evidence": "Economists often use the ceteris paribus or “other things being equal” assumption: while examining the economic impact of one event, all other factors remain unchanged for analysis purposes."}]

Final context:

```text
[e1e508c1c4c2696ee44b039c | data/day6/economics-chapters-3-4.pdf | PDF page 10]
held equal, then the laws of supply and demand will not necessarily hold, as the following Clear It Up feature shows. When does ceteris paribus apply? We typically apply ceteris paribus when we observe how changes in price affect demand or supply, but we can apply ceteris paribus more generally. In the real world, demand and supply depend on more factors than just price. For example, a consumer’s demand depends on income and a producer’s supply depends on the cost of producing the product. How can we analyze the effect on demand or supply if multiple factors are changing at the same time—say price rises and income falls? The answer is that we examine the changes one at a time, assuming the other factors are held constant. For example, we can say that an increase in the price reduces the amount consumers will buy (assuming income, and anything else that affects demand, is unchanged). 

[b707422cb03dc81d2cab1d30 | data/day6/economics-chapters-3-4.pdf | PDF page 9]
The more driving-age children a family has, the greater their demand for car insurance, and the less for diapers and baby formula. These factors matter for both individual and market demand as a whole. Exactly how do these various factors affect demand, and how do we show the effects graphically? To answer those questions, we need the ceteris paribus assumption. The Ceteris Paribus Assumption A demand curve or a supply curve is a relationship between two, and only two, variables: quantity on the horizontal axis and price on the vertical axis. The assumption behind a demand curve or a supply curve is that no relevant economic factors, other than the product’s price, are changing. Economists call this assumption ceteris paribus, a Latin phrase meaning “other things being equal.” Any given demand or supply curve is based on the ceteris paribus assumption that all else is held equal. 

[e23632d622cb83d2569ec2ee | data/day6/economics-chapters-3-4.pdf | PDF page 10]
Additionally, a decrease in income reduces the amount consumers can afford to buy (assuming price, and anything else that affects demand, is unchanged). This is what the ceteris paribus assumption really means. In this particular case, after we analyze each factor separately, we can combine the results. The amount consumers buy falls for two reasons: first because of the higher price and second because of the lower income. How Does Income Affect Demand? Let’s use income as an example of how factors other than price affect demand. Figure 3.5 shows the initial demand for automobiles as D0. At point Q, for example, if the price is $20,000 per car, the quantity of cars demanded is 18 million. D0 also shows how the quantity of cars demanded would change as a result of a higher or lower price. For example, if the price of a car rose to $22,000, the quantity demanded would decrease to 17 million, at point R. 

[57d1a4cd7538990d90f7ef0c | data/day6/economics-chapters-3-4.pdf | PDF page 33]
Key Terms ceteris paribus other things being equal complements goods that are often used together so that consumption of one good tends to enhance consumption of the other consumer surplus the extra benefit consumers receive from buying a good or service, measured by what the individuals would have been willing to pay minus the amount that they actually paid deadweight loss the loss in social surplus that occurs when a market produces an inefficient quantity demand the relationship between price and the quantity demanded of a certain good or service demand curve a graphic representation of the relationship between price and quantity demanded of a certain good or service, with quantity on the horizontal axis and the price on the vertical axis demand schedule a table that shows a range of prices for a certain good or service and the quantity demanded at each price economic surplus see social surplus equilibrium the situation where quantity demanded is equal to the quantity supplied; the

[4d3953793110140eb560f1fd | data/day6/economics-chapters-3-4.pdf | PDF page 34]
In either case, economic pressures will push the price toward the equilibrium level. 3.2 Shifts in Demand and Supply for Goods and Services Economists often use the ceteris paribus or “other things being equal” assumption: while examining the economic impact of one event, all other factors remain unchanged for analysis purposes. Factors that can shift the demand curve for goods and services, causing a different quantity to be demanded at any given price, include changes in tastes, population, income, prices of substitute or complement goods, and expectations about future conditions and prices. Factors that can shift the supply curve for goods and services, causing a different quantity to be supplied at any given price, include input prices, natural conditions, changes in technology, and government taxes, regulations, or subsidies. 
```

## d7-dev-q07

Hàng hóa thông thường được định nghĩa theo quan hệ giữa thu nhập và cầu như thế nào?

Status: answered

Expected answer/behavior: Thu nhập tăng thì cầu tăng và ngược lại.

Agent answer: Hàng hóa thông thường là hàng hóa mà **cầu tăng khi thu nhập tăng, và cầu giảm khi thu nhập giảm** [fe3ade2d487b951b3cb47418].

Citation IDs: ["fe3ade2d487b951b3cb47418"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 11, "evidence": "A product whose demand rises when income rises, and vice versa, is called a normal good."}, {"source_id": "openstax-principles-economics-3e", "page": 33, "evidence": "normal good a good in which the quantity demanded rises as income rises, and in which quantity demanded falls as income falls"}]

Final context:

```text
[9c9151fac0bd601b78b72fd7 | data/day6/economics-chapters-3-4.pdf | PDF page 11]
For some—luxury cars, vacations in Europe, and fine jewelry—the effect of a rise in income can be especially pronounced. A product whose demand rises when income rises, and vice versa, is called a normal good. A few exceptions to this pattern do exist. As incomes rise, many people will buy fewer

[d186b4cf738611e9f0bd60c1 | data/day6/economics-chapters-3-4.pdf | PDF page 33]
 combination of price and quantity where there is no economic pressure from surpluses or shortages that would cause price or quantity to change equilibrium price the price where quantity demanded is equal to quantity supplied equilibrium quantity the quantity at which quantity demanded and quantity supplied are equal for a certain price level excess demand at the existing price, the quantity demanded exceeds the quantity supplied; also called a shortage excess supply at the existing price, quantity supplied exceeds the quantity demanded; also called a surplus factors of production the resources such as labor, materials, and machinery that are used to produce goods and services; also called inputs inferior good a good in which the quantity demanded falls as income rises, and in which quantity demanded rises and income falls inputs the resources such as labor, materials, and machinery that are used to produce goods and services; also called factors of production law of demand the common

[fe3ade2d487b951b3cb47418 | data/day6/economics-chapters-3-4.pdf | PDF page 33]
 relationship that a higher price leads to a lower quantity demanded of a certain good or service and a lower price leads to a higher quantity demanded, while all other variables are held constant law of supply the common relationship that a higher price leads to a greater quantity supplied and a lower price leads to a lower quantity supplied, while all other variables are held constant normal good a good in which the quantity demanded rises as income rises, and in which quantity demanded falls as income falls price what a buyer pays for a unit of the specific good or service price ceiling a legal maximum price price control government laws to regulate prices instead of letting market forces determine prices price floor a legal minimum price producer surplus the extra benefit producers receive from selling a good or service, measured by the price the producer actually received minus the price the producer would have been willing to accept quantity demanded the total number of units of

[57d1a4cd7538990d90f7ef0c | data/day6/economics-chapters-3-4.pdf | PDF page 33]
Key Terms ceteris paribus other things being equal complements goods that are often used together so that consumption of one good tends to enhance consumption of the other consumer surplus the extra benefit consumers receive from buying a good or service, measured by what the individuals would have been willing to pay minus the amount that they actually paid deadweight loss the loss in social surplus that occurs when a market produces an inefficient quantity demand the relationship between price and the quantity demanded of a certain good or service demand curve a graphic representation of the relationship between price and quantity demanded of a certain good or service, with quantity on the horizontal axis and the price on the vertical axis demand schedule a table that shows a range of prices for a certain good or service and the quantity demanded at each price economic surplus see social surplus equilibrium the situation where quantity demanded is equal to the quantity supplied; the

[b97bb1949cbf6a611c130fcf | data/day6/economics-chapters-3-4.pdf | PDF page 13]
the store to stock up on coffee now. We show these changes in demand as shifts in the curve. Therefore, a shift in demand happens when a change in some economic factor (other than price) causes a different quantity to be demanded at every price. The following Work It Out feature shows how this happens. Shift in Demand A shift in demand means that at any price (and at every price), the quantity demanded will be different than it was before. Following is an example of a shift in demand due to an income increase. Step 1. Draw the graph of a demand curve for a normal good like pizza. Pick a price (like P0). Identify the corresponding Q0. See an example in Figure 3.6. FIGURE 3.6 Demand Curve We can use the demand curve to identify how much consumers would buy at any given price. Step 2. Suppose income increases. As a result of the change, are consumers going to buy more or less pizza? The answer is more. 
```

## d7-dev-q08

Đối với hàng hóa thứ cấp, thu nhập tăng làm đường cầu dịch chuyển ra sao?

Status: answered

Expected answer/behavior: Cầu giảm và đường cầu dịch sang trái.

Agent answer: Đối với hàng hóa thứ cấp, khi thu nhập tăng thì đường cầu dịch chuyển sang trái (cầu giảm). [202195399cb73d530929cc3b]

Citation IDs: ["202195399cb73d530929cc3b"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 12, "evidence": "A product whose demand falls when income rises, and vice versa, is called an inferior good. In other words, when income increases, the demand curve shifts to the left."}, {"source_id": "openstax-principles-economics-3e", "page": 33, "evidence": "inferior good a good in which the quantity demanded falls as income rises, and in which quantity demanded rises and income falls"}]

Final context:

```text
[202195399cb73d530929cc3b | data/day6/economics-chapters-3-4.pdf | PDF page 23]
A change in production costs caused a change in supply for the Postal Service. Step 3. Was the effect on supply positive or negative? Higher labor compensation leads to a lower quantity supplied of postal services at every given price, causing the supply curve for postal services to shift to the left, from S0 to S1. Step 4. Compare the new equilibrium price and quantity to the original equilibrium price. The new equilibrium (E1) occurs at a lower quantity and a higher price than the original equilibrium (E0). Figure 3.18 (b) shows the shift in demand in the following steps. Step 1. Draw a demand and supply model to illustrate what the market for U.S. Postal Services looked like before this scenario starts. The demand curve D0 and the supply curve S0 show the original relationships. Note that this diagram is independent from the diagram in panel (a). Step 2. Did the change described affect supply or demand? 

[cc374bf8ed83d6dc1a3305e6 | data/day6/economics-chapters-3-4.pdf | PDF page 21]
price is $3.25 per pound and the original equilibrium quantity is 250,000 fish. (This price per pound is what commercial buyers pay at the fishing docks. What consumers pay at the grocery is higher.) Step 2. Did the economic event affect supply or demand? Good weather is an example of a natural condition that affects supply. Step 3. Was the effect on supply an increase or a decrease? Good weather is a change in natural conditions that increases the quantity supplied at any given price. The supply curve shifts to the right, moving from the original supply curve S0 to the new supply curve S1, which Figure 3.16 and Table 3.6 show. Step 4. Compare the new equilibrium price and quantity to the original equilibrium. At the new equilibrium E1, the equilibrium price falls from $3.25 to $2.50, but the equilibrium quantity increases from 250,000 to 550,000 salmon. Notice that the equilibrium quantity demanded increased, even though the demand curve did not move. 

[8051fa4df46528c7c8aa47a7 | data/day6/economics-chapters-3-4.pdf | PDF page 16]
Now, imagine that the price of steel, an important ingredient in manufacturing cars, rises, so that producing a car has become more expensive. At any given price for selling cars, car manufacturers will react by supplying a lower quantity. We can show this graphically as a leftward shift of supply, from S0 to S1, which indicates that at any given price, the quantity supplied decreases. In this example, at a price of $20,000, the quantity supplied decreases from 18 million on the original supply curve (S0) to 16.5 million on the supply curve S1, which is labeled as point L. Conversely, if the price of steel decreases, producing a car becomes less expensive. At any given price for selling cars, car manufacturers can now expect to earn higher profits, so they will supply a higher quantity. The shift of supply to the right, from S0 to S2, means that at all prices, the quantity supplied has increased. 

[780caf36849ceb01eddf3e2f | data/day6/economics-chapters-3-4.pdf | PDF page 15]
Price Decrease to S1 Original Quantity Supplied S0 Increase to S2 $16,000 10.5 million 12.0 million 13.2 million $18,000 13.5 million 15.0 million 16.5 million $20,000 16.5 million 18.0 million 19.8 million $22,000 18.5 million 20.0 million 22.0 million $24,000 19.5 million 21.0 million 23.1 million $26,000 20.5 million 22.0 million 24.2 million TABLE 3.5 Price and Shifts in Supply: A Car Example

[263e69b5977b130444e5bbc2 | data/day6/economics-chapters-3-4.pdf | PDF page 48]
FIGURE 4.6 The United States as a Global Borrower Before U.S. Debt Uncertainty The graph shows the demand for financial capital from and supply of financial capital into the U.S. financial markets by the foreign sector before the increase in uncertainty regarding U.S. public debt. The original equilibrium (E0) occurs at an equilibrium rate of return (R0) and the equilibrium quantity is at Q0. Step 2. Will the diminished confidence in the U.S. economy as a place to invest affect demand or supply of financial capital? Yes, it will affect supply. Many foreign investors look to the U.S. financial markets to store their money in safe financial vehicles with low risk and stable returns. Diminished confidence means U.S. financial assets will be seen as more risky. Step 3. Will supply increase or decrease? When the enthusiasm of foreign investors’ for investing their money in the U.S. economy diminishes, the supply of financial capital shifts to the left. 
```

## d7-dev-q09

Nếu giá hàng hóa thay thế giảm thì cầu đối với sản phẩm còn lại thay đổi thế nào?

Status: answered

Expected answer/behavior: Cầu đối với sản phẩm còn lại giảm.

Agent answer: Giá hàng hóa thay thế giảm thì cầu đối với sản phẩm còn lại sẽ giảm. [d49553be9953d89f48f2e9eb]

Citation IDs: ["d49553be9953d89f48f2e9eb"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 12, "evidence": "A lower price for a substitute decreases demand for the other product."}]

Final context:

```text
[d49553be9953d89f48f2e9eb | data/day6/economics-chapters-3-4.pdf | PDF page 12]
A society with relatively more elderly persons, as the United States is projected to have by 2030, has a higher demand for nursing homes and hearing aids. Similarly, changes in the size of the population can affect the demand for housing and many other goods. Each of these changes in demand will be shown as a shift in the demand curve. Changes in the Prices of Related Goods Changes in the prices of related goods such as substitutes or complements also can affect the demand for a product. A substitute is a good or service that we can use in place of another good or service. As electronic books, like this one, become more available, you would expect to see a decrease in demand for traditional printed books. A lower price for a substitute decreases demand for the other product. For example, in recent years as the price of tablet computers has fallen, the quantity demanded has increased (because of the law of demand). 

[b2c0b3597dc79b22873b213d | data/day6/economics-chapters-3-4.pdf | PDF page 11]
In this case, the decrease in income would lead to a lower quantity of cars demanded at every given price, and the original demand curve D0 would shift left to D2. The shift from D0 to D2 represents such a decrease in demand: At any given price level, the quantity demanded is now lower. In this example, a price of $20,000 means 18 million cars sold along the original demand curve, but only 14.4 million sold after demand fell. When a demand curve shifts, it does not mean that the quantity demanded by every individual buyer changes by the same amount. In this example, not everyone would have higher or lower income and not everyone would buy or not buy an additional car. Instead, a shift in a demand curve captures a pattern for the market as a whole. In the previous section, we argued that higher income causes greater demand at every price. This is true for most goods and services. 

[4d3953793110140eb560f1fd | data/day6/economics-chapters-3-4.pdf | PDF page 34]
In either case, economic pressures will push the price toward the equilibrium level. 3.2 Shifts in Demand and Supply for Goods and Services Economists often use the ceteris paribus or “other things being equal” assumption: while examining the economic impact of one event, all other factors remain unchanged for analysis purposes. Factors that can shift the demand curve for goods and services, causing a different quantity to be demanded at any given price, include changes in tastes, population, income, prices of substitute or complement goods, and expectations about future conditions and prices. Factors that can shift the supply curve for goods and services, causing a different quantity to be supplied at any given price, include input prices, natural conditions, changes in technology, and government taxes, regulations, or subsidies. 

[3e9cfa16dec452a1fc4487d0 | data/day6/economics-chapters-3-4.pdf | PDF page 18]
Notice that a change in the price of the product itself is not among the factors that shift the supply curve. Although a change in price of a good or service typically causes a change in quantity supplied or a movement along the supply curve for that specific good or service, it does not cause the supply curve itself to shift.

[8051fa4df46528c7c8aa47a7 | data/day6/economics-chapters-3-4.pdf | PDF page 16]
Now, imagine that the price of steel, an important ingredient in manufacturing cars, rises, so that producing a car has become more expensive. At any given price for selling cars, car manufacturers will react by supplying a lower quantity. We can show this graphically as a leftward shift of supply, from S0 to S1, which indicates that at any given price, the quantity supplied decreases. In this example, at a price of $20,000, the quantity supplied decreases from 18 million on the original supply curve (S0) to 16.5 million on the supply curve S1, which is labeled as point L. Conversely, if the price of steel decreases, producing a car becomes less expensive. At any given price for selling cars, car manufacturers can now expect to earn higher profits, so they will supply a higher quantity. The shift of supply to the right, from S0 to S2, means that at all prices, the quantity supplied has increased. 
```

## d7-dev-q10

Chi phí sản xuất giảm tác động thế nào đến lượng cung tại mỗi mức giá và đường cung?

Status: answered

Expected answer/behavior: Lượng cung tại mỗi giá tăng; đường cung dịch sang phải.

Agent answer: Khi chi phí sản xuất giảm, doanh nghiệp sẽ cung cấp **nhiều hơn tại mỗi mức giá**; điều này làm **đường cung dịch sang phải**. Nói cách khác, ở mọi mức giá, lượng cung tăng lên và cung toàn thị trường tăng [bf99d2679cc71aa9000cb515].

Citation IDs: ["bf99d2679cc71aa9000cb515"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 15, "evidence": "When costs of production fall, a firm will tend to supply a larger quantity at any given price for its output. We can show this by the supply curve shifting to the right."}]

Final context:

```text
[8051fa4df46528c7c8aa47a7 | data/day6/economics-chapters-3-4.pdf | PDF page 16]
Now, imagine that the price of steel, an important ingredient in manufacturing cars, rises, so that producing a car has become more expensive. At any given price for selling cars, car manufacturers will react by supplying a lower quantity. We can show this graphically as a leftward shift of supply, from S0 to S1, which indicates that at any given price, the quantity supplied decreases. In this example, at a price of $20,000, the quantity supplied decreases from 18 million on the original supply curve (S0) to 16.5 million on the supply curve S1, which is labeled as point L. Conversely, if the price of steel decreases, producing a car becomes less expensive. At any given price for selling cars, car manufacturers can now expect to earn higher profits, so they will supply a higher quantity. The shift of supply to the right, from S0 to S2, means that at all prices, the quantity supplied has increased. 

[23f6ab8f2d2ff14b7b06d6d7 | data/day6/economics-chapters-3-4.pdf | PDF page 16]
In this example, at a price of $20,000, the quantity supplied increases from 18 million on the original supply curve (S0) to 19.8 million on the supply curve S2, which is labeled M. Other Factors That Affect Supply In the example above, we saw that changes in the prices of inputs in the production process will affect the cost of production and thus the supply. Several other things affect the cost of production, too, such as changes in weather or other natural conditions, new technologies for production, and some government policies. Changes in weather and climate will affect the cost of production for many agricultural products. For example, in 2014 the Manchurian Plain in Northeastern China, which produces most of the country's wheat, corn, and soybeans, experienced its most severe drought in 50 years. A drought decreases the supply of agricultural products, which means that at any given price, a lower quantity will be supplied. 

[a6acf59423a3cbe0238e615a | data/day6/economics-chapters-3-4.pdf | PDF page 39]
Those workers who do not adapt to changes in technology will experience a decrease in demand. Number of Companies An increase in the number of companies producing a given product will increase the demand for labor resulting in a shift to the right. A decrease in the number of companies producing a given product will decrease the demand for labor resulting in a shift to the left. Government Regulations Complying with government regulations can increase or decrease the demand for labor at any given wage. In the healthcare industry, government rules may require that nurses be hired to carry out certain medical procedures. This will increase the demand for nurses. Less-trained healthcare workers would be prohibited from carrying out these procedures, and the demand for these workers will shift to the left. Price and Availability of Other Inputs Labor is not the only input into the production process. 

[d92f5d8faec20a03ef6d7db8 | data/day6/economics-chapters-3-4.pdf | PDF page 8]
However, the below-equilibrium price reduces gasoline producers’ incentives to produce and sell gasoline, and the quantity supplied falls from 600 to 550.

[bf99d2679cc71aa9000cb515 | data/day6/economics-chapters-3-4.pdf | PDF page 16]
Higher costs decrease supply for the reasons we discussed above. Other examples of policy that can affect cost are the wide array of government regulations that require firms to spend money to provide a cleaner environment or a safer workplace. Complying with regulations increases costs. A government subsidy, on the other hand, is the opposite of a tax. A subsidy occurs when the government pays a firm directly or reduces the firm’s taxes if the firm carries out certain actions. From the firm’s perspective, taxes or regulations are an additional cost of production that shifts supply to the left, leading the firm to produce a lower quantity at every given price. Government subsidies reduce the cost of production and increase supply at every given price, shifting supply to the right. The following Work It Out feature shows how this shift happens. Shift in Supply We know that a supply curve shows the minimum price a firm will accept to produce a given quantity of output. 
```

## d7-dev-q11

Công nghệ mới giúp giảm chi phí sản xuất sẽ dịch chuyển đường cung theo hướng nào?

Status: answered

Expected answer/behavior: Sang phải, lượng sản xuất tại mỗi mức giá tăng.

Agent answer: Công nghệ mới làm giảm chi phí sản xuất sẽ làm **đường cung dịch chuyển sang phải**. [b680c3db6b3db4cac66e3aaf]

Citation IDs: ["b680c3db6b3db4cac66e3aaf"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 16, "evidence": "A technological improvement that reduces costs of production will shift supply to the right, so that a greater quantity will be produced at any given price."}]

Final context:

```text
[7a10c523fde773f4db6ada63 | data/day6/economics-chapters-3-4.pdf | PDF page 41]
Step 1. What did the markets for low-skill labor and high-skill labor look like before the arrival of the new technologies? In Figure 4.3 (a) and Figure 4.3 (b), S0 is the original supply curve for labor and D0 is the original demand curve for labor in each market. In each graph, the original point of equilibrium, E0, occurs at the price W0 and the quantity Q0. FIGURE 4.3 Technology and Wages: Applying Demand and Supply (a) The demand for low-skill labor shifts to the left when technology can do the job previously done by these workers. (b) New technologies can also increase the demand for high-skill labor in fields such as information technology and network administration. Step 2. Does the new technology affect the supply of labor from households or the demand for labor from firms? The technology change described here affects demand for labor by firms that hire workers. Step 3. Will the new technology increase or decrease demand? 

[99da734a555cbbc1ed8dbbae | data/day6/economics-chapters-3-4.pdf | PDF page 22]
What does this suggest for the future, given that two-thirds of Americans under 30 years old say they do not obtain their news from television at all? The Interconnections and Speed of Adjustment in Real Markets In the real world, many factors that affect demand and supply can change all at once. For example, the demand for cars might increase because of rising incomes and population, and it might decrease because of rising gasoline prices (a complementary good). Likewise, the supply of cars might increase because of innovative new technologies that reduce the cost of car production, and it might decrease as a result of new government regulations requiring the installation of costly pollution-control technology. Moreover, rising incomes and population or changes in gasoline prices will affect many markets, not just cars. How can an economist sort out all these interconnected events? The answer lies in the ceteris paribus assumption. 

[b680c3db6b3db4cac66e3aaf | data/day6/economics-chapters-3-4.pdf | PDF page 16]
Conversely, especially good weather would shift the supply curve to the right. When a firm discovers a new technology that allows the firm to produce at a lower cost, the supply curve will shift to the right, as well. For instance, in the 1960s a major scientific effort nicknamed the Green Revolution focused on breeding improved seeds for basic crops like wheat and rice. By the early 1990s, more than two- thirds of the wheat and rice in low-income countries around the world used these Green Revolution seeds—and the harvest was twice as high per acre. A technological improvement that reduces costs of production will shift supply to the right, so that a greater quantity will be produced at any given price. Government policies can affect the cost of production and the supply curve through taxes, regulations, and subsidies. For example, the U.S. government imposes a tax on alcoholic beverages that collects about $8 billion per year from producers. Businesses treat taxes as costs. 

[9ca2d182f91691f133e85121 | data/day6/economics-chapters-3-4.pdf | PDF page 41]
Based on the description earlier, as the substitute for low-skill labor becomes available, demand for low-skill labor will shift to the left, from D0 to D1. As the technology complement for high-skill labor becomes cheaper, demand for high-skill labor will shift to the right, from D0 to D1. Step 4. The new equilibrium for low-skill labor, shown as point E1 with price W1 and quantity Q1, has a lower wage and quantity hired than the original equilibrium, E0. The new equilibrium for high-skill labor, shown as point E1 with price W1 and quantity Q1, has a higher wage and quantity hired than the original equilibrium (E0). Thus, the demand and supply model predicts that the new computer and communications technologies will raise the pay of high-skill workers but reduce the pay of low-skill workers. From the 1970s to the mid-2000s, the wage gap widened between high-skill and low-skill labor. 

[67860e551395d8a8aa328b78 | data/day6/economics-chapters-3-4.pdf | PDF page 40]
How will the new technologies affect the wages of high-skill and low-skill workers? For this question, the four-step process of analyzing how shifts in supply or demand affect a market (introduced in Demand and Supply) works in this way:
```

## d7-dev-q12

Theo chương 3, giá trần là gì?

Status: answered

Expected answer/behavior: Mức giá tối đa hợp pháp được trả cho hàng hóa hoặc dịch vụ.

Agent answer: Theo chương 3, giá trần là mức giá tối đa hợp pháp mà người mua phải trả cho một hàng hóa hoặc dịch vụ; nói cách khác, đó là mức giá bị pháp luật không cho tăng vượt quá một ngưỡng nhất định. [16c345471555e9b2221913e2] [d8f05b4f3bcfa9e97aae6287]

Citation IDs: ["16c345471555e9b2221913e2", "d8f05b4f3bcfa9e97aae6287"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 26, "evidence": "A price ceiling is a legal maximum price that one pays for some good or service."}, {"source_id": "openstax-principles-economics-3e", "page": 33, "evidence": "price ceiling a legal maximum price"}]

Final context:

```text
[16c345471555e9b2221913e2 | data/day6/economics-chapters-3-4.pdf | PDF page 26]
Price Ceilings Laws that governments enact to regulate prices are called price controls. Price controls come in two flavors. A price ceiling keeps a price from rising above a certain level (the “ceiling”), while a price floor keeps a price from falling below a given level (the “floor”). This section uses the demand and supply framework to analyze price ceilings. The next section discusses price floors. A price ceiling is a legal maximum price that one pays for some good or service. A government imposes price ceilings in order to keep the price of some necessary good or service affordable. For example, in 2005 during Hurricane Katrina, the price of bottled water increased above $5 per gallon. As a result, many people called for price controls on bottled water to prevent the price from rising so high. In this particular case, the government did not impose a price ceiling, but there are other examples of where price ceilings did occur. 

[3f479e60fd5e54509bccc780 | data/day6/economics-chapters-3-4.pdf | PDF page 27]
At that price ($500), the quantity supplied remains at the same 15,000 rental units, but the quantity demanded is 19,000 rental units. In other words, the quantity demanded exceeds the quantity supplied, so there is a shortage of rental housing. One of the ironies of price ceilings is that while the price ceiling was intended to help renters, there are actually fewer apartments rented out under the price ceiling (15,000 rental units) than would be the case at the market rent of $600 (17,000 rental units). Price ceilings do not simply benefit renters at the expense of landlords. Rather, some renters (or potential renters) lose their housing as landlords convert apartments to co-ops and condos. Even when the housing remains in the rental market, landlords tend to spend less on maintenance and on essentials like heating, cooling, hot water, and lighting. The first rule of economics is you do not get something for nothing—everything has an opportunity cost. 

[7bd42d45ff60fed30470be9b | data/day6/economics-chapters-3-4.pdf | PDF page 27]
FIGURE 3.21 A Price Ceiling Example—Rent Control The original intersection of demand and supply occurs at E0. If demand shifts from D0 to D1, the new equilibrium would be at E1—unless a price ceiling prevents the price from rising. If the price is not permitted to rise, the quantity supplied remains at 15,000. However, after the change in demand, the quantity demanded rises to 19,000, resulting in a shortage. Price Original Quantity Supplied Original Quantity Demanded New Quantity Demanded $400 12,000 18,000 23,000 $500 15,000 15,000 19,000 $600 17,000 13,000 17,000 $700 19,000 11,000 15,000 $800 20,000 10,000 14,000 TABLE 3.7 Rent Control Suppose that a city government passes a rent control law to keep the price at the original equilibrium of $500 for a typical apartment. In Figure 3.21, the horizontal line at the price of $500 shows the legally fixed maximum price set by the rent control law. However, the underlying forces that shifted the demand curve to the right are still there. 

[d8f05b4f3bcfa9e97aae6287 | data/day6/economics-chapters-3-4.pdf | PDF page 34]
3.3 Changes in Equilibrium Price and Quantity: The Four-Step Process When using the supply and demand framework to think about how an event will affect the equilibrium price and quantity, proceed through four steps: (1) sketch a supply and demand diagram to think about what the market looked like before the event; (2) decide whether the event will affect supply or demand; (3) decide whether the effect on supply or demand is negative or positive, and draw the appropriate shifted supply or demand curve; (4) compare the new equilibrium price and quantity to the original ones. 3.4 Price Ceilings and Price Floors Price ceilings prevent a price from rising above a certain level. When a price ceiling is set below the equilibrium price, quantity demanded will exceed quantity supplied, and excess demand or shortages will result. Price floors prevent a price from falling below a certain level. 

[94a659e3a023e270ee84f3e2 | data/day6/economics-chapters-3-4.pdf | PDF page 2]
3 Demand and Supply BRING IT HOME
```

## d7-dev-q13

Giá sàn được định nghĩa như thế nào?

Status: answered

Expected answer/behavior: Giá thấp nhất được phép trả hợp pháp cho hàng hóa hoặc dịch vụ.

Agent answer: Giá sàn là mức giá thấp nhất mà người mua có thể hợp pháp trả cho một hàng hóa hoặc dịch vụ; nói cách khác, nó ngăn giá giảm xuống dưới một mức nhất định. [16c345471555e9b2221913e2][1a1e8171ef90020e9e97246c]

Citation IDs: ["16c345471555e9b2221913e2", "1a1e8171ef90020e9e97246c"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 28, "evidence": "A price floor is the lowest price that one can legally pay for some good or service."}, {"source_id": "openstax-principles-economics-3e", "page": 33, "evidence": "price floor a legal minimum price"}]

Final context:

```text
[1a1e8171ef90020e9e97246c | data/day6/economics-chapters-3-4.pdf | PDF page 28]
all. Quality is also likely to deteriorate. Price Floors A price floor is the lowest price that one can legally pay for some good or service. Perhaps the best-known example of a price floor is the minimum wage, which is based on the view that someone working full time should be able to afford a basic standard of living. The federal minimum wage in 2022 was $7.25 per hour, although some states and localities have a higher minimum wage. The federal minimum wage yields an annual income for a single person of $15,080, which is slightly higher than the Federal poverty line of $11,880. Congress periodically raises the federal minimum wage as the cost of living rises. As of March 2022, the most recent adjustment occurred in 2009, when the federal minimum wage was raised from $6.55 to $7.25. Price floors are sometimes called “price supports,” because they support a price by preventing it from falling below a certain level. 

[92e7ffe93d6b9824f26c5c21 | data/day6/economics-chapters-3-4.pdf | PDF page 31]
The original consumer surplus is G + H + J, and producer surplus is I + K. The city government is worried that movie theaters will go out of business, reducing the entertainment options available to citizens, so it decides to impose a price floor of $12 per ticket. As a result, the quantity demanded of movie tickets falls to 1,400. The new consumer surplus is G, and the new producer surplus is H + I. In effect, the price floor causes the area H to be transferred from consumer to producer surplus, but also causes a deadweight loss of J + K. This analysis shows that a price ceiling, like a law establishing rent controls, will transfer some producer surplus to consumers—which helps to explain why consumers often favor them. Conversely, a price floor like a guarantee that farmers will receive a certain price for their crops will transfer some consumer surplus to producers, which explains why producers often favor them. 

[369fe41a4b7daf8ec2dca382 | data/day6/economics-chapters-3-4.pdf | PDF page 34]
When a price floor is set above the equilibrium price, quantity supplied will exceed quantity demanded, and excess supply or surpluses will result. Price floors and price ceilings often lead to unintended consequences.

[4badbe3a11e178637560a1fb | data/day6/economics-chapters-3-4.pdf | PDF page 31]
Note that the gain to consumers is less than the loss to producers, which is just another way of seeing the deadweight loss. FIGURE 3.24 Efficiency and Price Floors and Ceilings (a) The original equilibrium price is $600 with a quantity of 20,000. Consumer surplus is T + U, and producer surplus is V + W + X. A price ceiling is imposed at $400, so firms in the market now produce only a quantity of 15,000. As a result, the new consumer surplus is T + V, while the new producer surplus is X. (b) The original equilibrium is $8 at a quantity of 1,800. Consumer surplus is G + H + J, and producer surplus is I + K. A price floor is imposed at $12, which means that quantity demanded falls to 1,400. As a result, the new consumer surplus is G, and the new producer surplus is H + I. Figure 3.24 (b) shows a price floor example using a string of struggling movie theaters, all in the same city. The current equilibrium is $8 per movie ticket, with 1,800 people attending movies. 

[16c345471555e9b2221913e2 | data/day6/economics-chapters-3-4.pdf | PDF page 26]
Price Ceilings Laws that governments enact to regulate prices are called price controls. Price controls come in two flavors. A price ceiling keeps a price from rising above a certain level (the “ceiling”), while a price floor keeps a price from falling below a given level (the “floor”). This section uses the demand and supply framework to analyze price ceilings. The next section discusses price floors. A price ceiling is a legal maximum price that one pays for some good or service. A government imposes price ceilings in order to keep the price of some necessary good or service affordable. For example, in 2005 during Hurricane Katrina, the price of bottled water increased above $5 per gallon. As a result, many people called for price controls on bottled water to prevent the price from rising so high. In this particular case, the government did not impose a price ceiling, but there are other examples of where price ceilings did occur. 
```

## d7-dev-q14

Thặng dư xã hội được tính từ những thành phần nào?

Status: answered

Expected answer/behavior: Tổng thặng dư tiêu dùng và thặng dư sản xuất.

Agent answer: Thặng dư xã hội được tính bằng **tổng của thặng dư tiêu dùng và thặng dư sản xuất** [16108ea89f238f980195d8ec][14b1e8c207cb81b597e0586f].

Citation IDs: ["16108ea89f238f980195d8ec", "14b1e8c207cb81b597e0586f"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 30, "evidence": "The sum of consumer surplus and producer surplus is social surplus, also referred to as economic surplus or total surplus."}, {"source_id": "openstax-principles-economics-3e", "page": 34, "evidence": "social surplus the sum of consumer surplus and producer surplus"}]

Final context:

```text
[16108ea89f238f980195d8ec | data/day6/economics-chapters-3-4.pdf | PDF page 30]
Those producers who would have been willing to supply the tablets at $45, but who were instead able to charge the equilibrium price of $80, clearly received an extra benefit beyond what they required to supply the product. The extra benefit producers receive from selling a good or service, measured by the price the producer actually received minus the price the producer would have been willing to accept is called producer surplus. In Figure 3.23, producer surplus is the area labeled G—that is, the area between the market price and the segment of the supply curve below the equilibrium. The sum of consumer surplus and producer surplus is social surplus, also referred to as economic surplus or total surplus. In Figure 3.23 we show social surplus as the area F + G. Social surplus is larger at equilibrium quantity and price than it would be at any other quantity. This demonstrates the economic efficiency of the market equilibrium. 

[2eb737a838f1853157d967b0 | data/day6/economics-chapters-3-4.pdf | PDF page 31]
As a result, two changes occur. First, an inefficient outcome occurs and the total surplus of society is reduced. The loss in social surplus that occurs when the economy produces at an inefficient quantity is called deadweight loss. In a very real sense, it is like money thrown away that benefits no one. In Figure 3.24 (a), the deadweight loss is the area U + W. When deadweight loss exists, it is possible for both consumer and producer surplus to be higher, in this case because the price control is blocking some suppliers and demanders from transactions they would both be willing to make. A second change from the price ceiling is that some of the producer surplus is transferred to consumers. After the price ceiling is imposed, the new consumer surplus is T + V, while the new producer surplus is X. In other words, the price ceiling transfers the area of surplus (V) from producers to consumers. 

[57d1a4cd7538990d90f7ef0c | data/day6/economics-chapters-3-4.pdf | PDF page 33]
Key Terms ceteris paribus other things being equal complements goods that are often used together so that consumption of one good tends to enhance consumption of the other consumer surplus the extra benefit consumers receive from buying a good or service, measured by what the individuals would have been willing to pay minus the amount that they actually paid deadweight loss the loss in social surplus that occurs when a market produces an inefficient quantity demand the relationship between price and the quantity demanded of a certain good or service demand curve a graphic representation of the relationship between price and quantity demanded of a certain good or service, with quantity on the horizontal axis and the price on the vertical axis demand schedule a table that shows a range of prices for a certain good or service and the quantity demanded at each price economic surplus see social surplus equilibrium the situation where quantity demanded is equal to the quantity supplied; the

[14b1e8c207cb81b597e0586f | data/day6/economics-chapters-3-4.pdf | PDF page 34]
demand social surplus the sum of consumer surplus and producer surplus substitute a good that can replace another to some extent, so that greater consumption of one good can mean less of the other supply the relationship between price and the quantity supplied of a certain good or service supply curve a line that shows the relationship between price and quantity supplied on a graph, with quantity supplied on the horizontal axis and price on the vertical axis supply schedule a table that shows a range of prices for a good or service and the quantity supplied at each price surplus at the existing price, quantity supplied exceeds the quantity demanded; also called excess supply total surplus see social surplus Key Concepts and Summary 3.1 Demand, Supply, and Equilibrium in Markets for Goods and Services A demand schedule is a table that shows the quantity demanded at different prices in the market. 
```

## d7-dev-q15

Theo chương 4, ai cung ứng và ai có nhu cầu lao động?

Status: answered

Expected answer/behavior: Người tìm việc cung ứng lao động; doanh nghiệp và bên tuyển dụng có cầu lao động.

Agent answer: Theo chương 4, **hộ gia đình** là bên **cung ứng lao động**, còn **doanh nghiệp (các hãng tuyển dụng)** là bên **có nhu cầu lao động** [feada1dac01f6e024a0b1533].

Citation IDs: ["feada1dac01f6e024a0b1533"]

Gold source evidence: [{"source_id": "openstax-principles-economics-3e", "page": 36, "evidence": "In labor markets job seekers (individuals) are the suppliers of labor, while firms and other employers who hire labor are the demanders for labor."}]

Final context:

```text
[7a10c523fde773f4db6ada63 | data/day6/economics-chapters-3-4.pdf | PDF page 41]
Step 1. What did the markets for low-skill labor and high-skill labor look like before the arrival of the new technologies? In Figure 4.3 (a) and Figure 4.3 (b), S0 is the original supply curve for labor and D0 is the original demand curve for labor in each market. In each graph, the original point of equilibrium, E0, occurs at the price W0 and the quantity Q0. FIGURE 4.3 Technology and Wages: Applying Demand and Supply (a) The demand for low-skill labor shifts to the left when technology can do the job previously done by these workers. (b) New technologies can also increase the demand for high-skill labor in fields such as information technology and network administration. Step 2. Does the new technology affect the supply of labor from households or the demand for labor from firms? The technology change described here affects demand for labor by firms that hire workers. Step 3. Will the new technology increase or decrease demand? 

[feada1dac01f6e024a0b1533 | data/day6/economics-chapters-3-4.pdf | PDF page 36]
As this chapter will illustrate, we can analyze labor markets and financial markets with the same tools we use to analyze demand and supply in the goods markets. 4.1 Demand and Supply at Work in Labor Markets LEARNING OBJECTIVES By the end of this section, you will be able to: • Predict shifts in the demand and supply curves of the labor market • Explain the impact of new technology on the demand and supply curves of the labor market • Explain price floors in the labor market such as minimum wage or a living wage Markets for labor have demand and supply curves, just like markets for goods. The law of demand applies in labor markets this way: A higher salary or wage—that is, a higher price in the labor market—leads to a decrease in the quantity of labor demanded by employers, while a lower salary or wage leads to an increase in the quantity of labor demanded. 

[9ca2d182f91691f133e85121 | data/day6/economics-chapters-3-4.pdf | PDF page 41]
Based on the description earlier, as the substitute for low-skill labor becomes available, demand for low-skill labor will shift to the left, from D0 to D1. As the technology complement for high-skill labor becomes cheaper, demand for high-skill labor will shift to the right, from D0 to D1. Step 4. The new equilibrium for low-skill labor, shown as point E1 with price W1 and quantity Q1, has a lower wage and quantity hired than the original equilibrium, E0. The new equilibrium for high-skill labor, shown as point E1 with price W1 and quantity Q1, has a higher wage and quantity hired than the original equilibrium (E0). Thus, the demand and supply model predicts that the new computer and communications technologies will raise the pay of high-skill workers but reduce the pay of low-skill workers. From the 1970s to the mid-2000s, the wage gap widened between high-skill and low-skill labor. 

[67860e551395d8a8aa328b78 | data/day6/economics-chapters-3-4.pdf | PDF page 40]
How will the new technologies affect the wages of high-skill and low-skill workers? For this question, the four-step process of analyzing how shifts in supply or demand affect a market (introduced in Demand and Supply) works in this way:

[07d951bd8d858e72ffe7b3bf | data/day6/economics-chapters-3-4.pdf | PDF page 35]
FIGURE 4.1 People often think of demand and supply in relation to goods, but labor markets, such as the nursing profession, can also apply to this analysis. (Credit: modification of "Hospital do Subúrbio" by Jaques Wagner Governador/Flickr Creative Commons, CC BY 2.0) Chapter Objectives In this chapter, you will learn about: • Demand and Supply at Work in Labor Markets • Demand and Supply in Financial Markets • The Market System as an Efficient Mechanism for Information Introduction to Labor and Financial Markets Baby Boomers Come of Age According to the 2020 Census, 22% of the U.S. population was 60 years old or older, which means that more than 74 million people have reached an age when they will need increased medical care. The baby boomer population, the group born between 1946 and 1964, is comprised of more than 71 million people who have already reached retirement age or will soon reach retirement. 
```

## d7-dev-u01

Theo bộ tài liệu này, mức lương tối thiểu vùng I của Việt Nam năm 2026 chính xác là bao nhiêu đồng/tháng?

Status: error

Expected answer/behavior: Corpus không cung cấp quy định lương tối thiểu vùng I Việt Nam năm 2026.

Agent answer: 

Citation IDs: []

Gold source evidence: []

Final context:

```text
[e2a84937a58dee8155989009 | data/day6/economics-chapters-3-4.pdf | PDF page 42]
government definition of what it means for a family to be in poverty. (A family with two adults earning minimum wage and two young children will find it more cost efficient for one parent to provide childcare while the other works for income. Thus the family income would be $14,500, which is significantly lower than the federal poverty line for a family of four, which was $26,500 in 2021.) Supporters of the living wage argue that full-time workers should be assured a high enough wage so that they can afford the essentials of life: food, clothing, shelter, and healthcare. Since Baltimore passed the first living wage law in 1994, several dozen cities enacted similar laws in the late 1990s and the 2000s. The living wage ordinances do not apply to all employers, but they have specified that all employees of the city or employees of firms that the city hires be paid at least a certain wage that is usually a few dollars per hour above the U.S. minimum wage. 

[32b87bc877697d1beba92fd2 | data/day6/economics-chapters-3-4.pdf | PDF page 42]
people from earning income are not politically popular. There is one exception: boards of trustees or stockholders, as an example, propose limits on the high incomes of top business executives. The labor market, however, presents some prominent examples of price floors, which are an attempt to increase the wages of low-paid workers. The U.S. government sets a minimum wage, a price floor that makes it illegal for an employer to pay employees less than a certain hourly rate. In mid-2009, the U.S. minimum wage was raised to $7.25 per hour. Local political movements in a number of U.S. cities have pushed for a higher minimum wage, which they call a living wage. Promoters of living wage laws maintain that the minimum wage is too low to ensure a reasonable standard of living. They base this conclusion on the calculation that, if you work 40 hours a week at a minimum wage of $7.25 per hour for 50 weeks a year, your annual income is $14,500, which is less than the official U.S. 

[7ffcf9efc3df4e5521562d46 | data/day6/economics-chapters-3-4.pdf | PDF page 43]
Wage Quantity Labor Demanded Quantity Labor Supplied $8/hr 1,900 500 $9/hr 1,500 900 $10/hr 1,200 1,200 $11/hr 900 1,400 $12/hr 700 1,600 $13/hr 500 1,800 $14/hr 400 1,900 TABLE 4.4 Living Wage: Example of a Price Floor The Minimum Wage as an Example of a Price Floor The U.S. minimum wage is a price floor that is set either very close to the equilibrium wage or even slightly below it. About 1.5% of hourly workers in the U.S. are paid the minimum wage. In other words, the vast majority of the U.S. labor force has its wages determined in the labor market, not as a result of the government price floor. However, for workers with low skills and little experience, like those without a high school diploma or teenagers, the minimum wage is quite important. In many cities, the federal minimum wage is apparently below the market price for unskilled labor, because employers offer more than the minimum wage to checkout clerks and other low-skill workers without any government prodding. 

[9ca2d182f91691f133e85121 | data/day6/economics-chapters-3-4.pdf | PDF page 41]
Based on the description earlier, as the substitute for low-skill labor becomes available, demand for low-skill labor will shift to the left, from D0 to D1. As the technology complement for high-skill labor becomes cheaper, demand for high-skill labor will shift to the right, from D0 to D1. Step 4. The new equilibrium for low-skill labor, shown as point E1 with price W1 and quantity Q1, has a lower wage and quantity hired than the original equilibrium, E0. The new equilibrium for high-skill labor, shown as point E1 with price W1 and quantity Q1, has a higher wage and quantity hired than the original equilibrium (E0). Thus, the demand and supply model predicts that the new computer and communications technologies will raise the pay of high-skill workers but reduce the pay of low-skill workers. From the 1970s to the mid-2000s, the wage gap widened between high-skill and low-skill labor. 
```

## d7-dev-u02

Theo tài liệu, hệ số co giãn cầu theo giá của xăng tại Việt Nam năm 2025 chính xác bằng bao nhiêu?

Status: abstain

Expected answer/behavior: Ví dụ xăng không cung cấp ước lượng co giãn thực nghiệm cho Việt Nam năm 2025.

Agent answer: Không đủ bằng chứng trong tài liệu được cung cấp để trả lời câu hỏi này.

Citation IDs: []

Gold source evidence: []

Final context:

```text
[4e2ddf8ef33cd2cf11668c7a | data/day6/economics-chapters-3-4.pdf | PDF page 3]
LINK IT UP Visit this website (https://openstax.org/l/celebauction) to read a list of bizarre items that have been purchased for their ties to celebrities. These examples represent an interesting facet of demand and supply. When economists talk about prices, they are less interested in making judgments than in gaining a practical understanding of what determines prices and why prices change. Consider a price most of us contend with weekly: that of a gallon of gas. Why was the average price of gasoline in the United States $3.16 per gallon in June of 2020? Why did the price for gasoline fall sharply to $2.42 per gallon by January of 2021? To explain these price movements, economists focus on the determinants of what gasoline buyers are willing to pay and what gasoline sellers are willing to accept. As it turns out, the price of gasoline in June of any given year is nearly always higher than the price in January of that same year. 

[a3b41552dad761a0db8abbc1 | data/day6/economics-chapters-3-4.pdf | PDF page 10]
The original demand curve D0, like every demand curve, is based on the ceteris paribus assumption that no other economically relevant factors change. Now imagine that the economy expands in a way that raises the incomes of many people, making cars more affordable. How will this affect demand? How can we show this graphically? Return to Figure 3.5. The price of cars is still $20,000, but with higher incomes, the quantity demanded has now increased to 20 million cars, shown at point S. As a result of the higher income levels, the demand curve shifts to the right to the new demand curve D1, indicating an increase in demand. Table 3.4 shows clearly that this increased demand would occur at every price, not just the original one. CLEAR IT UP

[99da734a555cbbc1ed8dbbae | data/day6/economics-chapters-3-4.pdf | PDF page 22]
What does this suggest for the future, given that two-thirds of Americans under 30 years old say they do not obtain their news from television at all? The Interconnections and Speed of Adjustment in Real Markets In the real world, many factors that affect demand and supply can change all at once. For example, the demand for cars might increase because of rising incomes and population, and it might decrease because of rising gasoline prices (a complementary good). Likewise, the supply of cars might increase because of innovative new technologies that reduce the cost of car production, and it might decrease as a result of new government regulations requiring the installation of costly pollution-control technology. Moreover, rising incomes and population or changes in gasoline prices will affect many markets, not just cars. How can an economist sort out all these interconnected events? The answer lies in the ceteris paribus assumption. 

[8fe35f29f0a234a94791774b | data/day6/economics-chapters-3-4.pdf | PDF page 15]
As a result, a higher cost of production typically causes a firm to supply a smaller quantity at any given price. In this case, the supply curve shifts to the left. Consider the supply for cars, shown by curve S0 in Figure 3.10. Point J indicates that if the price is $20,000, the quantity supplied will be 18 million cars. If the price rises to $22,000 per car, ceteris paribus, the quantity supplied will rise to 20 million cars, as point K on the S0 curve shows. We can show the same information in table form, as in Table 3.5. FIGURE 3.10 Shifts in Supply: A Car Example Decreased supply means that at every given price, the quantity supplied is lower, so that the supply curve shifts to the left, from S0 to S1. Increased supply means that at every given price, the quantity supplied is higher, so that the supply curve shifts to the right, from S0 to S2. 

[a82898c46ebd459e8b89c69c | data/day6/economics-chapters-3-4.pdf | PDF page 7]
Figure 3.4 illustrates the interaction of demand and supply in the market for gasoline. The demand curve (D) is identical to Figure 3.2. The supply curve (S) is identical to Figure 3.3. Table 3.3 contains the same information in tabular form. FIGURE 3.4 Demand and Supply for Gasoline The demand curve (D) and the supply curve (S) intersect at the equilibrium point E, with a price of $1.40 and a quantity of 600. The equilibrium price is the only price where quantity demanded is equal to quantity supplied. At a price above equilibrium like $1.80, quantity supplied exceeds the quantity demanded, so there is excess supply. At a price below equilibrium such as $1.20, quantity demanded exceeds quantity supplied, so there is excess demand. Price (per gallon) Quantity demanded (millions of gallons) Quantity supplied (millions of gallons) $1.00 800 500 $1.20 700 550 $1.40 600 600 TABLE 3.3 Price, Quantity Demanded, and Quantity Supplied
```
