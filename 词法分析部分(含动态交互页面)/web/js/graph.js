var DFA;
var NFA;
var TITLE;
var NODE;
var END;
var CANJUDGE=false; //false
var JUDGEBUTTON=true;  //true
var STRINDEX=0;  //0
var status=-1;  //-1
var INTERVAL=null; //null
var JUDGESENTENCE;
//生成图像的操作：
function getNFA()
{
    var NFAG = new dagreD3.graphlib.Graph()
        .setGraph({})
        .setDefaultEdgeLabel(function() { return {}; });
    for(var i=0;i<NFA.length;i++) {
        if (NODE[i] == 2) {
            NFAG.setNode(i, {label: String(i), class: "type-end"});
        }
        else {
            if (NODE[i] == 1) {
                NFAG.setNode(i, {label: String(i), class: "type-no"});
            }
            if (NODE[i] == 3) {
                NFAG.setNode(i, {label: String(i), class: "type-begin"});
            }
        }
    }
    NFAG.nodes().forEach(function(v) {
        var node = NFAG.node(v);
        node.rx = node.ry = 5;
    });
    for(var i=0;i<NFA.length;i++) {
        if (NODE[i] == 0)
            continue;
        for (var j = 0; j < NFA[i].length; j++) {
            for (var k = 0; k < NFA[i][j].length; k++) {
                NFAG.setEdge(i, NFA[i][j][k], {label: TITLE[j+1]});
            }
        }
    }
    var render = new dagreD3.render();
    var NFAsvg = d3.select("#svg1"),
        NFAsvgGroup = NFAsvg.append("g");
    render(d3.select("#svg1 g"), NFAG);
    var xCenterOffsetNFA = (NFAsvg.attr("width") - NFAG.graph().width) / 2;
    NFAsvgGroup.attr("transform", "translate(" + xCenterOffsetNFA + ", 20)");
    NFAsvg.attr("height", NFAG.graph().height + 40);
}
function getDFA(ok) {
    var DFAG = new dagreD3.graphlib.Graph()
        .setGraph({})
        .setDefaultEdgeLabel(function() { return {}; });
    console.log(status);
    for(var i=0;i<DFA.length;i++) {
        if (i == status&&ok)
            DFAG.setNode(DFA[i][0][0], {label: String(DFA[i][0][0]), class: "type-active"})
        else {
            if (END[i])
                DFAG.setNode(DFA[i][0][0], {label: String(DFA[i][0][0]), class: "type-end"})
            else
            {
                if(i==0)
                    DFAG.setNode(DFA[i][0][0], {label: String(DFA[i][0][0]), class: "type-begin"})
                else
                    DFAG.setNode(DFA[i][0][0],{label:String(DFA[i][0][0]),class:"type-no"});
            }
        }
    }
    DFAG.nodes().forEach(function(v) {
        var node = DFAG.node(v);
        node.rx = node.ry = 5;
    });
    self=new Array();
    for(var i=0;i<DFA.length;i++) {
        for (var j = 1; j < DFA[i].length; j++) {
            for (var k = 0; k < DFA[i][j].length; k++) {
                if (DFA[i][0][0] == DFA[i][j][k]) {
                    var add = true;
                    for (var m = 0; m < self.length; m++) {
                        if (self[m].node == DFA[i][0][0]) {
                            add = false;
                            self[m].label.push(TITLE[j]);
                        }
                    }
                    if (add) {
                        var temp = {};
                        temp.node = DFA[i][0][0];
                        temp.label = new Array();
                        temp.label.push(TITLE[j]);
                        self.push(temp);
                    }
                }
                else
                    DFAG.setEdge(DFA[i][0][0], DFA[i][j][k], {label: TITLE[j]});
            }
        }
    }
    for(var i=0;i<self.length;i++)
        DFAG.setEdge(self[i].node,self[i].node,{label:String(self[i].label)})
    var render = new dagreD3.render();
    var DFAsvg = d3.select("#svg2"),
        DFAsvgGroup = DFAsvg.append("g");
    render(d3.select("#svg2 g"), DFAG);
    var xCenterOffsetDFA = (DFAsvg.attr("width") - DFAG.graph().width) / 2;
    DFAsvgGroup.attr("transform", "translate(" + xCenterOffsetDFA + ", 20)");
    DFAsvg.attr("height", DFAG.graph().height + 40);
}
function getStandard(nfa,dfa)
{
    console.log("form server response data:")
    console.log(nfa);
    console.log(dfa);
    console.log(TITLE);
    console.log("after change in client:")
    NFA=new Array();
    NODE=new Array();
    for(var i=0;i<nfa.length;i++)
        NODE.push(0);
    for(var i=0;i<nfa.length;i++) {
        NFA.push(new Array());
        for (var j = 0; j < nfa[i].length; j++) {
            temp = nfa[i][j].substr(1, nfa[i][j].length - 2);
            temp = temp.split(",");
            arr = new Array();
            if (temp[0] != "") {
                for (var k = 0; k < temp.length; k++) {
                    arr.push(Number(temp[k]));
                    NODE[Number(temp[k])] = 1;
                }
                NFA[i].push(arr);
            }
            else {
                NFA[i].push(arr);
            }
        }
    }
    for(var i=0;i<NFA.length;i++) {
        empty = true;
        for (var j = 0; j < NFA[i].length; j++) {
            if (NFA[i][j].length != 0) {
                empty = false;
                break;
            }
        }
        if (empty && NODE[i] == 1) {
            NODE[i] = 2;
        }
        if(!empty && NODE[i]==0)
        {
            NODE[i]=3;
        }
    }
    console.log("NFA and NODE");
    console.log(NFA);
    console.log(NODE);
    DFA=new Array();
    END=new Array();
    for(var i=0;i<dfa.length;i++)
    {
        END.push(false);
        if(dfa[i][0][dfa[i][0].length-1]=="*")
        {
            END[i]=true;
        }
    }
    for(var i=0;i<dfa.length;i++)
    {
        DFA.push(new Array());
        for(var j=0;j<dfa[i].length;j++)
        {
            if(dfa[i][j]=="-1")
            {
                arr=new Array();
                DFA[i].push(arr);
            }
            else
            {
                //如果是接受状态：
                if(dfa[i][j][dfa[i][j].length-1]=="*")
                {
                    arr=new Array();
                    arr.push(Number(dfa[i][j].substr(0,dfa[i][j].length-1)));
                    DFA[i].push(arr);
                }
                //如果是普通状态：
                else
                {
                    arr=new Array();
                    arr.push(Number(dfa[i][j]));
                    DFA[i].push(arr);
                }
            }
        }
    }
    console.log("DFA and END");
    console.log(DFA);
    console.log(END);
}
//提交一个新的正则表达式之后要进行的操作。
function Ajax()
{
    if(INTERVAL!=null)
        window.clearInterval(INTERVAL)
    string =$("#string").val();
    if(string!="") {
        $.post("Machine", {'string': string}, function (data, status) {
            $("#svg1").empty();
            $("#svg2").empty();
            $("#set").empty();
            status=-1;
            nfa=data[1];
            dfa=data[0];
            TITLE=data[2];
            TITLE.push("#");
            getStandard(nfa,dfa);
            getNFA();
            getDFA(false);
            CANJUDGE=true;
            JUDGEBUTTON=true;
        }, "json");
    }
    else {
        alert("please input a regular expression!");
    }
}
function setSet(string) {
    var data="";
    for(var i=0;i<string.length;i++)
    {
        if(STRINDEX==i)
            data+="<span class='word active'>"+string[i]+"</span>";
        else
            data+="<span class='word'>"+string[i]+"</span>";
    }
    $("#set").empty();
    $("#set").html(data);

    $("#svg2").empty();
    var index=TITLE.indexOf(JUDGESENTENCE[STRINDEX]);
    //当前字符在输入集合中找不到
    if(index==-1) {
        alert("fail! ");
        window.clearInterval(INTERVAL);
    }
    else
    {
        if(DFA[status][index].length==0)
        {
            alert("fail !");
            window.clearInterval(INTERVAL);
        }
        else
        {
            status=DFA[status][index][0];
            STRINDEX++;
        }
    }
    getDFA(true);
}

function judge() {
    JUDGESENTENCE = $("#target").val();
    if(JUDGESENTENCE!="") {
        if (CANJUDGE && JUDGEBUTTON) {
            JUDGEBUTTON = false;
            if (target == "") {
                alert("Input a string please");
            }
            else {
                STRINDEX = 0;
                status = DFA[0][0][0];
                success = false;
                INTERVAL = setInterval(function () {
                    setSet(JUDGESENTENCE);
                    //changeDFA();
                    if (STRINDEX == JUDGESENTENCE.length && END[status]) {
                        alert("success");
                        success = true;
                    }
                    if (success)
                        window.clearInterval(INTERVAL);
                }, 2000);
            }
        }
        else
            alert("can not judge before build! ");
    }
    else
        alert("please input a string to judge!");
}