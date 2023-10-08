import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
class ChatMessage extends StatelessWidget {
  const ChatMessage({
    super.key,
    this.text,
    this.name,
    this.type,
  });

  final String? text;
  final String? name;
  final bool? type;

  List<Widget> otherMessage(context) {
    return <Widget>[
      Container(
        margin: const EdgeInsets.only(right: 5.0),
        child: const CircleAvatar(child: Icon(Icons.support_agent_rounded)),
      ),
      Container(
        padding: EdgeInsets.all(10),

        decoration: BoxDecoration(
        color: Colors.grey[300],
        borderRadius: BorderRadius.only(
        topRight: Radius.circular(18),
        bottomLeft: Radius.circular(18),
        bottomRight: Radius.circular(18),
        ),
        ),
        child: Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Text(
                name ?? "",
                style: const TextStyle(fontSize: 17,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Container(
                margin: const EdgeInsets.only(top: 8.0),
                child: ConstrainedBox(
                  constraints: BoxConstraints(
                    // minWidth: 300.0,
                    maxWidth: MediaQuery.of(context).size.width/1.5,
                    // minHeight: 30.0,
                   // maxHeight: 100.0,
                  ),
                child: AutoSizeText(text ?? "",
                    style: TextStyle(fontSize: 15)),
              )
              ),
            ],
          ),
        ),
      ),
    ];
  }

  List<Widget> myMessage(context) {
    return <Widget>[
      Expanded(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: <Widget>[
            Container(
              padding: EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: Colors.cyan[100],
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(18),
                  bottomLeft: Radius.circular(18),
                  bottomRight: Radius.circular(18),
                ),
              ),
              margin: const EdgeInsets.only(top: 5.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(name ?? "", style: TextStyle(fontSize: 17,fontWeight: FontWeight.bold)),
                  Container(
                    margin: const EdgeInsets.only(top: 8.0),
                    child: ConstrainedBox(
                      constraints: BoxConstraints(
                        // minWidth: 300.0,
                        maxWidth: MediaQuery.of(context).size.width,
                        // minHeight: 30.0,
                       // maxHeight: 100.0,
                      ),
                    child: AutoSizeText(text ?? "",
                    style: TextStyle(fontSize: 15),),
                  )
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      Container(
        margin: const EdgeInsets.only(left: 8.0),
        child: CircleAvatar(
            child: Icon(Icons.person_2_outlined)
        ),
      ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 10.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: type ?? false ? myMessage(context) : otherMessage(context),
      ),
    );
  }
}